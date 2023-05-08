from matplotlib import pyplot as plt

def display_bgr(title, image):
	plt.figure()
	plt.title(title)
	plt.imshow(image[:, :, [2, 1, 0]])

def display_upscales(name, images, ratios=False):
	n = len(images)

	if ratios:
		width_ratios = [2 ** i for i in range(n)]
		fig, axs = plt.subplots(1, n, figsize=(15, 15), gridspec_kw={'width_ratios': width_ratios})
	else:
		fig, axs = plt.subplots(1, n, figsize=(15, 15))

	for i in range(n):
		axs[i].imshow(images[i][:, :, [2, 1, 0]])
		if i == 0:
			title = "Original " + name
			axs[0].set_title(title)
		else:
			title = name + " " + str(2 ** i) + "x"
			axs[i].set_title(title)
