from config.database import execute_query

# Test connection by fetching projects
try:
    print("Testing database connection...")
    
    projects = execute_query("SELECT * FROM projects")
    
    print(f"\\n✓ Connection successful!")
    print(f"Found {len(projects)} projects:\\n")
    
    for project in projects:
        print(f"- {project['name']} ({project['country']})")
    
    print("\\n✓ Database setup is working perfectly!")
    
except Exception as e:
    print(f"\\n✗ Error: {e}")
    print("\\nCheck your .env file and DATABASE_URL")