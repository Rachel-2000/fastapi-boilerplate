cov:
	coverage run -m pytest
	coverage html

test:
	set ENV=test&& pytest tests -s
