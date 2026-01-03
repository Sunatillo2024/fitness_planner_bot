.PHONY: install run clean db-reset help

help:
	@echo "🏋️ Fitness Planner Bot - Makefile Commands"
	@echo ""
	@echo "  make install    - O'rnatish (dependencies)"
	@echo "  make run        - Botni ishga tushirish"
	@echo "  make clean      - Cache tozalash"
	@echo "  make db-reset   - Database'ni tozalash"
	@echo ""

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Installation complete!"

run:
	@echo "🚀 Starting bot..."
	python bot.py

clean:
	@echo "🧹 Cleaning cache..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cache cleaned!"

db-reset:
	@echo "⚠️  Resetting database..."
	rm -f fitness.db
	@echo "✅ Database reset!"