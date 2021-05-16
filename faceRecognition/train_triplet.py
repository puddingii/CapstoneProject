import numpy as np
import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torch.nn.modules.distance import PairwiseDistance
from datasets.LFWDataset import LFWDataset
from losses.triplet_loss import TripletLoss
from datasets.TripletLossDataset import TripletFaceDataset
from validate_on_LFW import evaluate_lfw
from plot import plot_roc_lfw, plot_accuracy_lfw
from tqdm import tqdm
from models.resnet import Resnet18Triplet


args = {'dataroot': '/content/dat_masked', 'lfw': '/content/lfwdata-masked-rename', 'dataset_csv': '/content/datasets/vggface2.csv', 'epochs': 70, 'iterations_per_epoch': 1000, 'model_architecture': 'resnet18', 'pretrained': False, 'embedding_dimension': 256,
        'num_human_identities_per_batch': 16, 'batch_size': 64, 'lfw_batch_size': 64, 'resume_path': '', 'num_workers': 2, 'optimizer': "adam", 'learning_rate': 0.1, 'margin': 0.2, 'image_size': 224, 'use_semihard_negatives': True, 'training_triplets_path': None
        }


def set_model_architecture(pretrained, embedding_dimension):
    model = Resnet18Triplet(
        embedding_dimension=embedding_dimension,
        pretrained=pretrained
    )
    print("Using resnet18 model architecture.")

    return model


def set_model_gpu_mode(model):
    flag_train_gpu = torch.cuda.is_available()
    flag_train_multi_gpu = False

    if flag_train_gpu and torch.cuda.device_count() > 1:
        model = nn.DataParallel(model)
        model.cuda()
        flag_train_multi_gpu = True
        print('Using multi-gpu training.')

    elif flag_train_gpu and torch.cuda.device_count() == 1:
        model.cuda()
        print('Using single-gpu training.')

    return model, flag_train_multi_gpu


def set_optimizer(optimizer, model, learning_rate):
    if optimizer == "adagrad":
        optimizer_model = optim.Adagrad(
            params=model.parameters(),
            lr=learning_rate,
            lr_decay=0,
            initial_accumulator_value=0.1,
            eps=1e-10
        )

    elif optimizer == "adam":
        optimizer_model = optim.Adam(
            params=model.parameters(),
            lr=learning_rate,
            betas=(0.9, 0.999),
            eps=1e-08,
            amsgrad=False
        )

    return optimizer_model


def validate_lfw(model, lfw_dataloader, model_architecture, epoch, epochs):
    model.eval()
    with torch.no_grad():
        l2_distance = PairwiseDistance(p=2)
        distances, labels = [], []

        print("Validating on LFW! ...")
        progress_bar = enumerate(tqdm(lfw_dataloader))

        for batch_index, (data_a, data_b, label) in progress_bar:
            data_a = data_a.cuda()
            data_b = data_b.cuda()

            output_a, output_b = model(data_a), model(data_b)
            distance = l2_distance.forward(
                output_a, output_b)  # Euclidean distance

            distances.append(distance.cpu().detach().numpy())
            labels.append(label.cpu().detach().numpy())

        labels = np.array([sublabel for label in labels for sublabel in label])
        distances = np.array(
            [subdist for distance in distances for subdist in distance])

        true_positive_rate, false_positive_rate, precision, recall, accuracy, roc_auc, best_distances, \
            tar, far = evaluate_lfw(
                distances=distances,
                labels=labels,
                far_target=1e-3
            )
        # Print statistics and add to log
        print("Accuracy on LFW: {:.4f}+-{:.4f}\tPrecision {:.4f}+-{:.4f}\tRecall {:.4f}+-{:.4f}\t"
              "ROC Area Under Curve: {:.4f}\tBest distance threshold: {:.2f}+-{:.2f}\t"
              "TAR: {:.4f}+-{:.4f} @ FAR: {:.4f}".format(
                  np.mean(accuracy),
                  np.std(accuracy),
                  np.mean(precision),
                  np.std(precision),
                  np.mean(recall),
                  np.std(recall),
                  roc_auc,
                  np.mean(best_distances),
                  np.std(best_distances),
                  np.mean(tar),
                  np.std(tar),
                  np.mean(far)
              )
              )
        with open('logs/lfw_{}_log_triplet.txt'.format(model_architecture), 'a') as f:
            val_list = [
                epoch,
                np.mean(accuracy),
                np.std(accuracy),
                np.mean(precision),
                np.std(precision),
                np.mean(recall),
                np.std(recall),
                roc_auc,
                np.mean(best_distances),
                np.std(best_distances),
                np.mean(tar)
            ]
            log = '\t'.join(str(value) for value in val_list)
            f.writelines(log + '\n')

    try:
        # Plot ROC curve
        plot_roc_lfw(
            false_positive_rate=false_positive_rate,
            true_positive_rate=true_positive_rate,
            figure_name="plots/roc_plots/roc_{}_epoch_{}_triplet.png".format(
                model_architecture, epoch)
        )
        # Plot LFW accuracies plot
        plot_accuracy_lfw(
            log_dir="logs/lfw_{}_log_triplet.txt".format(model_architecture),
            epochs=epochs,
            figure_name="plots/lfw_accuracies_{}_triplet.png".format(
                model_architecture)
        )
    except Exception as e:
        print(e)

    return best_distances


def forward_pass(imgs, model, batch_size):
    imgs = imgs.cuda()
    embeddings = model(imgs)

    # Split the embeddings into Anchor, Positive, and Negative embeddings
    anc_embeddings = embeddings[:batch_size]
    pos_embeddings = embeddings[batch_size: batch_size * 2]
    neg_embeddings = embeddings[batch_size * 2:]

    return anc_embeddings, pos_embeddings, neg_embeddings, model


def main():
    dataroot = args['dataroot']
    lfw_dataroot = args['lfw']
    dataset_csv = args['dataset_csv']
    epochs = args['epochs']
    iterations_per_epoch = args['iterations_per_epoch']
    model_architecture = args['model_architecture']
    pretrained = args['pretrained']
    embedding_dimension = args['embedding_dimension']
    num_human_identities_per_batch = args['num_human_identities_per_batch']
    batch_size = args['batch_size']
    lfw_batch_size = args['lfw_batch_size']
    resume_path = args['resume_path']
    num_workers = args['num_workers']
    optimizer = args['optimizer']
    learning_rate = args['learning_rate']
    margin = args['margin']
    image_size = args['image_size']
    use_semihard_negatives = args['use_semihard_negatives']
    training_triplets_path = args['training_triplets_path']
    flag_training_triplets_path = False
    start_epoch = 0

    if training_triplets_path is not None:
        # Load triplets file for the first training epoch
        flag_training_triplets_path = True

    # Define image data pre-processing transforms
    #   ToTensor() normalizes pixel values between [0, 1]
    #   Normalize(mean=[0.6068, 0.4517, 0.3800], std=[0.2492, 0.2173, 0.2082]) normalizes pixel values to be mean
    #    of zero and standard deviation of 1 according to the calculated VGGFace2 with tightly-cropped faces
    #    dataset RGB channels' mean and std values by calculate_vggface2_rgb_mean_std.py in 'datasets' folder.
    data_transforms = transforms.Compose([
        transforms.Resize(size=image_size),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(degrees=5),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.5916, 0.5268, 0.4842],
            std=[0.2615, 0.2649, 0.2869]
            # mean=[0.6068, 0.4517, 0.3800],
            # std=[0.2492, 0.2173, 0.2082]
        )
    ])

    lfw_transforms = transforms.Compose([
        transforms.Resize(size=image_size),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.5916, 0.5268, 0.4842],
            std=[0.2615, 0.2649, 0.2869]
        )
    ])

    lfw_dataloader = torch.utils.data.DataLoader(
        dataset=LFWDataset(
            dir=lfw_dataroot,
            pairs_path='datasets/LFW_pairs.txt',
            transform=lfw_transforms
        ),
        batch_size=lfw_batch_size,
        num_workers=num_workers,
        shuffle=False
    )

    # Instantiate model
    model = set_model_architecture(
        pretrained=pretrained,
        embedding_dimension=embedding_dimension
    )

    # Load model to GPU or multiple GPUs if available
    model, flag_train_multi_gpu = set_model_gpu_mode(model)

    # Set optimizer
    optimizer_model = set_optimizer(
        optimizer=optimizer,
        model=model,
        learning_rate=learning_rate
    )

    # Resume from a model checkpoint
    if resume_path:
        if os.path.isfile(resume_path):
            print("Loading checkpoint {} ...".format(resume_path))
            checkpoint = torch.load(resume_path)
            start_epoch = checkpoint['epoch'] + 1
            optimizer_model.load_state_dict(
                checkpoint['optimizer_model_state_dict'])

            # In order to load state dict for optimizers correctly, model has to be loaded to gpu first
            if flag_train_multi_gpu:
                model.module.load_state_dict(checkpoint['model_state_dict'])
            else:
                model.load_state_dict(checkpoint['model_state_dict'])
            print("Checkpoint loaded: start epoch from checkpoint = {}".format(
                start_epoch))
        else:
            print("WARNING: No checkpoint found at {}!\nTraining from scratch.".format(
                resume_path))

    if use_semihard_negatives:
        print("Using Semi-Hard negative triplet selection!")
    else:
        print("Using Hard negative triplet selection!")

    start_epoch = start_epoch

    print("Training using triplet loss starting for {} epochs:\n".format(
        epochs - start_epoch))

    for epoch in range(start_epoch, epochs):
        num_valid_training_triplets = 0
        l2_distance = PairwiseDistance(p=2)
        _training_triplets_path = None

        if flag_training_triplets_path:
            _training_triplets_path = training_triplets_path
            # Only load triplets file for the first epoch
            flag_training_triplets_path = False

        # Re-instantiate training dataloader to generate a triplet list for this training epoch
        train_dataloader = torch.utils.data.DataLoader(
            dataset=TripletFaceDataset(
                root_dir=dataroot,
                csv_name=dataset_csv,
                num_triplets=iterations_per_epoch * batch_size,
                num_human_identities_per_batch=num_human_identities_per_batch,
                triplet_batch_size=batch_size,
                epoch=epoch,
                training_triplets_path=_training_triplets_path,
                transform=data_transforms
            ),
            batch_size=batch_size,
            num_workers=num_workers,
            shuffle=False  # Shuffling for triplets with set amount of human identities per batch is not required
        )

        # Training pass
        model.train()
        progress_bar = enumerate(tqdm(train_dataloader))

        for batch_idx, (batch_sample) in progress_bar:

            # Forward pass - compute embeddings
            anc_imgs = batch_sample['anc_img']
            pos_imgs = batch_sample['pos_img']
            neg_imgs = batch_sample['neg_img']

            # Concatenate the input images into one tensor because doing multiple forward passes would create
            #  weird GPU memory allocation behaviours later on during training which would cause GPU Out of Memory
            #  issues
            # Must be a tuple of Torch Tensors
            all_imgs = torch.cat((anc_imgs, pos_imgs, neg_imgs))

            anc_embeddings, pos_embeddings, neg_embeddings, model = forward_pass(
                imgs=all_imgs,
                model=model,
                batch_size=batch_size
            )

            pos_dists = l2_distance.forward(anc_embeddings, pos_embeddings)
            neg_dists = l2_distance.forward(anc_embeddings, neg_embeddings)

            if use_semihard_negatives:
                # Semi-Hard Negative triplet selection
                #  (negative_distance - positive_distance < margin) AND (positive_distance < negative_distance)
                #   Based on: https://github.com/davidsandberg/facenet/blob/master/src/train_tripletloss.py#L295
                first_condition = (neg_dists - pos_dists <
                                   margin).cpu().numpy().flatten()
                second_condition = (
                    pos_dists < neg_dists).cpu().numpy().flatten()
                all = (np.logical_and(first_condition, second_condition))
                valid_triplets = np.where(all == 1)
            else:
                # Hard Negative triplet selection
                #  (negative_distance - positive_distance < margin)
                #   Based on: https://github.com/davidsandberg/facenet/blob/master/src/train_tripletloss.py#L296
                all = (neg_dists - pos_dists < margin).cpu().numpy().flatten()
                valid_triplets = np.where(all == 1)

            anc_valid_embeddings = anc_embeddings[valid_triplets]
            pos_valid_embeddings = pos_embeddings[valid_triplets]
            neg_valid_embeddings = neg_embeddings[valid_triplets]

            # Calculate triplet loss
            triplet_loss = TripletLoss(margin=margin).forward(
                anchor=anc_valid_embeddings,
                positive=pos_valid_embeddings,
                negative=neg_valid_embeddings
            )

            # Calculating number of triplets that met the triplet selection method during the epoch
            num_valid_training_triplets += len(anc_valid_embeddings)

            # Backward pass
            optimizer_model.zero_grad()
            triplet_loss.backward()
            optimizer_model.step()

        # Print training statistics for epoch and add to log
        print('Epoch {}:\tNumber of valid training triplets in epoch: {}'.format(
            epoch,
            num_valid_training_triplets
        )
        )

        with open('logs/{}_log_triplet.txt'.format(model_architecture), 'a') as f:
            val_list = [
                epoch,
                num_valid_training_triplets
            ]
            log = '\t'.join(str(value) for value in val_list)
            f.writelines(log + '\n')

        # Evaluation pass on LFW dataset
        best_distances = validate_lfw(
            model=model,
            lfw_dataloader=lfw_dataloader,
            model_architecture=model_architecture,
            epoch=epoch,
            epochs=epochs
        )

        # Save model checkpoint
        state = {
            'epoch': epoch,
            'embedding_dimension': embedding_dimension,
            'batch_size_training': batch_size,
            'model_state_dict': model.state_dict(),
            'model_architecture': model_architecture,
            'optimizer_model_state_dict': optimizer_model.state_dict(),
            'best_distance_threshold': np.mean(best_distances)
        }

        # For storing data parallel model's state dictionary without 'module' parameter
        if flag_train_multi_gpu:
            state['model_state_dict'] = model.module.state_dict()

        # Save model checkpoint
        torch.save(state, 'model_training_checkpoints/model_{}_triplet_epoch_{}.pt'.format(
            model_architecture,
            epoch
        )
        )


if __name__ == '__main__':
    main()
