import math
import torch 
import torch.nn as nn


class Gaussian_NLL(nn.Module):
	"""
	Negative log likelihood (loss function) of gaussian random variable

	: param y_true:     target value
	: param y_pred:     tuple(mu, sigma)
	: param mu:         mean of distribution ... size = (batch_size, output_dim)
	: param sigma:      standard deviation of distribution  ... size (batch_size, 1) <– same variance

	returns mean loss per sample (not per point)
	"""
	def __init__(self, reduction="mean"):
		super(Gaussian_NLL, self).__init__()
		self.reduction = reduction
		
	def forward(self, y_pred, y_true):
		assert len(y_pred)==2
		mu, sigma = y_pred

		log_px = torch.distributions.Normal(loc=mu, scale=sigma).log_prob(y_true)
		nll = - torch.sum(log_px, axis=-1) # neglog-likelihood (3D per channel, 2D per sample)
		
		if self.reduction=="mean":
			return torch.mean(nll) # 3D tensor -> mean per channels as well as per batch
		if self.reduction=="none":
			return nll


def gaussian_nll(y_true, mu, sigma):
	"""
	Negative log likelihood (loss function) of gaussian random variable

	: param y_true: 	target value
	: param mu: 		mean of distribution ... size = (batch_size, output_dim)
	: param sigma: 		standard deviation of distribution  ... size (batch_size, 1) <– same variance
	
	returns mean loss per sample (not per point)
	"""
	dim = mu.shape[1]/2
	var = sigma.pow(2)
	#print(mu.shape, sigma.shape)
	return torch.mean(torch.sum((y_true-mu).pow(2), axis=1)/(2*var) + dim*torch.log(var)) + dim*math.log(2*math.pi)


def sample_mse(y_true, y_pred):
	return torch.mean(torch.sum((y_true-y_pred).pow(2), axis=1))