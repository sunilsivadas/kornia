import pytest

import torch
from torch.testing import assert_allclose
from torch.autograd import gradcheck

from kornia.feature import SOSNet
import kornia.testing as utils  # test utils


class TestSOSNet:
    def test_shape(self, device):
        inp = torch.ones(1, 1, 32, 32, device=device)
        sosnet = SOSNet(pretrained=False).to(device)
        sosnet.eval()  # batchnorm with size 1 is not allowed in train mode
        out = sosnet(inp)
        assert out.shape == (1, 128)

    def test_shape_batch(self, device):
        inp = torch.ones(16, 1, 32, 32, device=device)
        sosnet = SOSNet(pretrained=False).to(device)
        out = sosnet(inp)
        assert out.shape == (16, 128)

    @pytest.mark.skip("jacobian not well computed")
    def test_gradcheck(self, device):
        patches = torch.rand(2, 1, 32, 32, device=device)
        patches = utils.tensor_to_gradcheck_var(patches)  # to var
        sosnet = SOSNet(pretrained=False).to(patches.device, patches.dtype)
        assert gradcheck(sosnet, (patches,), eps=1e-4, atol=1e-4,
                         raise_exception=True, )
