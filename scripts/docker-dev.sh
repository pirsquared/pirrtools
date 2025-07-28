#!/bin/bash

# Docker Development Script for pirrtools
# This script helps manage the development container with all modern tools

set -e

CONTAINER_NAME="pirrtools-dev"
IMAGE_NAME="pirrtools:dev"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m' 
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}🐳 pirrtools Docker Development Environment${NC}"
    echo "============================================="
}

print_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     - Build the development container"
    echo "  start     - Start the development container"
    echo "  stop      - Stop the development container"
    echo "  restart   - Restart the development container"  
    echo "  shell     - Open a shell in the running container"
    echo "  logs      - Show container logs"
    echo "  clean     - Remove container and images"
    echo "  test      - Run tests in container"
    echo "  lint      - Run linting in container"
    echo "  format    - Run code formatting in container"
    echo "  docs      - Build documentation in container"
    echo "  status    - Show container status"
    echo ""
}

build_container() {
    echo -e "${YELLOW}📦 Building development container...${NC}"
    docker-compose build --no-cache
    echo -e "${GREEN}✅ Container built successfully!${NC}"
}

start_container() {
    echo -e "${YELLOW}🚀 Starting development container...${NC}"
    docker-compose up -d
    echo -e "${GREEN}✅ Container started!${NC}"
    echo -e "${BLUE}📖 Documentation will be available at: http://localhost:8080${NC}"
    echo -e "${BLUE}🔧 Run '$0 shell' to open a development shell${NC}"
}

stop_container() {
    echo -e "${YELLOW}🛑 Stopping development container...${NC}"
    docker-compose down
    echo -e "${GREEN}✅ Container stopped!${NC}"
}

restart_container() {
    echo -e "${YELLOW}🔄 Restarting development container...${NC}"
    docker-compose restart
    echo -e "${GREEN}✅ Container restarted!${NC}"
}

open_shell() {
    if ! docker ps | grep -q $CONTAINER_NAME; then
        echo -e "${RED}❌ Container is not running. Starting it first...${NC}"
        start_container
        sleep 3
    fi
    echo -e "${BLUE}🐚 Opening development shell...${NC}"
    docker-compose exec pirrtools-dev /bin/bash
}

show_logs() {
    echo -e "${BLUE}📋 Container logs:${NC}"
    docker-compose logs -f
}

clean_container() {
    echo -e "${YELLOW}🧹 Cleaning up containers and images...${NC}"
    docker-compose down -v --rmi all
    echo -e "${GREEN}✅ Cleanup complete!${NC}"
}

run_tests() {
    echo -e "${YELLOW}🧪 Running tests...${NC}"
    docker-compose exec pirrtools-dev pytest --cov=pirrtools --cov-report=term-missing
}

run_lint() {
    echo -e "${YELLOW}🔍 Running linting...${NC}"
    docker-compose exec pirrtools-dev ruff check pirrtools/ tests/
}

run_format() {
    echo -e "${YELLOW}🎨 Running code formatting...${NC}"
    docker-compose exec pirrtools-dev black pirrtools/ tests/
    docker-compose exec pirrtools-dev isort pirrtools/ tests/
}

build_docs() {
    echo -e "${YELLOW}📚 Building documentation...${NC}"
    docker-compose exec pirrtools-dev make -C docs html
    echo -e "${GREEN}✅ Documentation built! Available at http://localhost:8080${NC}"
}

show_status() {
    echo -e "${BLUE}📊 Container Status:${NC}"
    if docker ps | grep -q $CONTAINER_NAME; then
        echo -e "${GREEN}✅ Container is running${NC}"
        docker ps | grep $CONTAINER_NAME
    else
        echo -e "${RED}❌ Container is not running${NC}"
    fi
}

# Main script logic
case "${1:-}" in
    "build")
        print_header
        build_container
        ;;
    "start")
        print_header  
        start_container
        ;;
    "stop")
        print_header
        stop_container
        ;;
    "restart")
        print_header
        restart_container
        ;;
    "shell")
        open_shell
        ;;
    "logs")
        show_logs
        ;;
    "clean")
        print_header
        clean_container
        ;;
    "test")
        run_tests
        ;;
    "lint")
        run_lint
        ;;
    "format")
        run_format
        ;;
    "docs")
        build_docs
        ;;
    "status")
        print_header
        show_status
        ;;
    "")
        print_header
        print_usage
        ;;
    *)
        print_header
        echo -e "${RED}❌ Unknown command: $1${NC}"
        echo ""
        print_usage
        exit 1
        ;;
esac