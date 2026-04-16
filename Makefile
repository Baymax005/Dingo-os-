.PHONY: help build clean test install

help:
	@echo "Dingo OS Build System"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build           Build all utilities"
	@echo "  task-manager    Build only Task Manager"
	@echo "  clean           Remove all build artifacts"
	@echo "  test            Run basic tests"
	@echo "  install         Install utilities to /usr/local/bin"
	@echo "  help            Show this message"

build: build-task-manager build-showip
	@echo "✓ All utilities built"

build-task-manager:
	@echo "Building Task Manager..."
	cd src/task-manager && make

build-showip:
	@echo "Preparing showip..."
	chmod +x src/showip/showip.sh
	@echo "✓ showip ready"

clean:
	@echo "Cleaning build artifacts..."
	cd src/task-manager && make clean
	rm -rf build/bin/*
	@echo "✓ Cleaned"

test: build
	@echo "Testing Task Manager..."
	./build/bin/task-manager --help
	@echo ""
	@echo "Testing showip..."
	./src/showip/showip.sh --help
	@echo "✓ Basic tests passed"

install: build
	@echo "Installing utilities..."
	sudo cp build/bin/task-manager /usr/local/bin/
	sudo cp src/showip/showip.sh /usr/local/bin/showip
	sudo chmod +x /usr/local/bin/showip
	@echo "✓ Installed to /usr/local/bin/"
	@echo "  Run 'task-manager' or 'showip' from anywhere"
