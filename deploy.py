import torch
import torchvision
from torch import nn
from torchvision import transforms

class Predict:
    def __init__(self, path_to_file=None, path_to_output_file=None):
        self.path_to_file = path_to_file
        self.path_to_output_file = path_to_output_file

    class TinyVGGm(nn.Module):
        def __init__(self):
            super().__init__()
            self.model = nn.Sequential(
                nn.Conv2d(3, 16, kernel_size=3, padding=1),
                nn.Conv2d(16, 16, kernel_size=3, padding=1),
                nn.Conv2d(16, 16, kernel_size=3, padding=1),
                nn.LeakyReLU(0.01),
                nn.BatchNorm2d(16),
                nn.Conv2d(16, 32, kernel_size=3),
                nn.LeakyReLU(0.01),
                nn.MaxPool2d(kernel_size=2, stride=2),

                nn.BatchNorm2d(32),
                nn.Conv2d(32, 64, kernel_size=3),
                nn.LeakyReLU(0.01),
                nn.BatchNorm2d(64),
                nn.Conv2d(64, 128, kernel_size=3),
                nn.LeakyReLU(0.01),
                nn.MaxPool2d(kernel_size=2, stride=2),

                nn.BatchNorm2d(128),
                nn.Conv2d(128, 128, kernel_size=3),
                nn.Dropout(0.33),

                nn.Flatten(),
                nn.Linear(46208, 2)
            )

        def forward(self, x):
            return self.model(x)

    def make_prediction(self):
        if not self.path_to_file or not self.path_to_output_file:
            raise ValueError("path_to_file and path_to_output_file must be provided")

        data_transform = transforms.Compose([
            transforms.Resize(size=(96, 96)),
        ])
        device = 'cuda' if torch.cuda.is_available() else 'cpu'

        class_names = ['0', '1']
        custom_image = data_transform(torchvision.io.read_image(str(self.path_to_file)) / 255).unsqueeze(dim=0)

        m1 = self.TinyVGGm()
        m1.load_state_dict(torch.load("model.pt", weights_only=True))

        m1.eval()
        with torch.inference_mode():
            custom_image_pred = m1(custom_image.to(device))

        custom_image_pred_class = class_names[torch.argmax(torch.softmax(custom_image_pred, dim=1), dim=1).cpu()]

        with open(self.path_to_output_file, 'w') as f:
            f.write(custom_image_pred_class)