test:
	@$(MAKE) -sk test-all

test-all:	test-wc test-diff

test-wc:
	@echo "word counting..."
	@./test_wc.py

test-diff:
	@echo "diff testing..."
	@./test_diff.py

clean:
	@echo "cleaning..."
	@rm testfile.txt
