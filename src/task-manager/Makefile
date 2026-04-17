CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2
SRCDIR = src
OBJDIR = obj
BINDIR = ../../../build/bin

SOURCES = $(SRCDIR)/main.cpp $(SRCDIR)/process.cpp
OBJECTS = $(SOURCES:$(SRCDIR)/%.cpp=$(OBJDIR)/%.o)
TARGET = $(BINDIR)/task-manager

# Default target
all: $(BINDIR) $(OBJDIR) $(TARGET)

# Create directories if they don't exist
$(BINDIR):
	mkdir -p $(BINDIR)

$(OBJDIR):
	mkdir -p $(OBJDIR)

# Link
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^
	@echo "✓ Built: $@"

# Compile
$(OBJDIR)/%.o: $(SRCDIR)/%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean
clean:
	rm -rf $(OBJDIR)
	rm -f $(TARGET)
	@echo "✓ Cleaned"

# Run (requires sudo to list all processes)
run: $(TARGET)
	$(TARGET)

.PHONY: all clean run
