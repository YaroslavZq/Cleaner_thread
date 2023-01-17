from time import time
from multiprocessing import cpu_count, Pool


def factorize(*number) -> dict:
	output = {}
	for i in number:
		division_list = []
		min_number = 1

		while min_number <= i:
			if i % min_number == 0:
				division_list.append(min_number)
				min_number += 1
			else:
				min_number += 1
		output[i] = division_list
	return output


if __name__ == '__main__':
	cpu = cpu_count()
	before_normal = time()
	result = factorize(128, 255, 99999, 10651060)
	print(f'Time taken normal: {time() - before_normal}')
	print(result)
	before_multiproc = time()
	pool = Pool(cpu)
	result = pool.apply_async(factorize, (128, 255, 99999, 10651060))
	print(f"Time taken with {cpu} cpu's {time() - before_multiproc}")
	print(result.get())
