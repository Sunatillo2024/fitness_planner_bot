"""
Database Migration Script
Adds missing full_name column to users table
"""
import sqlite3
import sys


def migrate_database():
    """Add full_name column to users table"""
    try:
        # Connect to database
        conn = sqlite3.connect('fitness.db')
        cursor = conn.cursor()

        # Check if column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'full_name' in columns:
            print("✅ Column 'full_name' already exists!")
            return

        # Add the missing column
        print("📝 Adding 'full_name' column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN full_name VARCHAR")

        # Update existing records with a default value
        cursor.execute("UPDATE users SET full_name = 'User' WHERE full_name IS NULL")

        conn.commit()
        print("✅ Migration completed successfully!")

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    print("=" * 50)
    print("🔧 Starting database migration...")
    print("=" * 50)

    migrate_database()

    print("=" * 50)
    print("🎉 Migration finished!")
    print("=" * 50)