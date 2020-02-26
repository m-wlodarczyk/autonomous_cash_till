import imageio
import glob
from imgaug import augmenters as iaa


def make_augmentation(path_read='AugNewRawData_288_352/*.bmp'):
    files = sorted(glob.glob(path_read))
    all_files = len(files)
    counter = 0

    for file in files:
        counter += 1

        image = imageio.imread(file)

        degrees = []
        images = []
        for it in range(11):
            images.append(image)

        sometimes = lambda aug: iaa.Sometimes(0.7, aug)

        seq = iaa.Sequential([
            sometimes(
                iaa.OneOf([
                    iaa.Dropout(p=(0, 0.05)),
                    iaa.CoarseDropout((0.0, 0.05), size_percent=(0.02, 0.25))
                ])
            ),
            # iaa.OneOf([
            #     iaa.GaussianBlur(sigma=(0.0, 1.5)),
            #     iaa.BilateralBlur(d=(3, 10), sigma_color=(10, 250), sigma_space=(10, 250)),
            #     iaa.AverageBlur(k=(2, 4)),
            # ]),
            iaa.Multiply((0.9, 1.1), per_channel=0.2),
            iaa.contrast.LinearContrast((0.9, 1.2)),
            iaa.AdditiveGaussianNoise(scale=(0, 10)),
            iaa.Grayscale(alpha=(0.0, 0.3)),
            iaa.CropAndPad(px=(-50, 50))
        ])

        images_aug = seq.augment_images(images)

        name = file.split(".")[0]
        for i, image_aug in enumerate(images_aug):
            imageio.imwrite(f"{name}_%d.bmp" % (i,), image_aug)
