#!/usr/bin/env python3
"""Test script to verify team member insertion"""

from config.database import execute_query

# Check how many members exist
query = "SELECT COUNT(*) as count FROM team_members"
result = execute_query(query)
print(f"Total members in database: {result[0]['count']}")

# Get all member IDs
query = "SELECT id, name, position, role_type, is_active FROM team_members ORDER BY id"
result = execute_query(query)
print(f"\nAll members:")
for member in result:
    print(f"  ID {member['id']}: {member['name']} - {member['position']} ({member['role_type']}) - Active: {member['is_active']}")

# Try to insert a test member
print("\n--- Inserting test member ---")
insert_query = """
    INSERT INTO team_members (name, position, role_type, bio, is_active, order_position)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id
"""
params = ('Test Member', 'Test Position', 'executive', 'Test bio', True, 0)
try:
    result = execute_query(insert_query, params, fetch=False)
    print(f"Insert result: {result}")
    
    if result and len(result) > 0:
        new_id = result[0]['id']
        print(f"New member ID: {new_id}")
        
        # Check total count again
        count_query = "SELECT COUNT(*) as count FROM team_members"
        count_result = execute_query(count_query)
        print(f"Total members after insert: {count_result[0]['count']}")
        
        # Verify it was inserted
        verify_query = "SELECT * FROM team_members WHERE id = %s"
        verification = execute_query(verify_query, (new_id,))
        print(f"Verification by ID: {verification}")
        
        # Try getting all and look for it
        all_query = "SELECT id, name FROM team_members ORDER BY id DESC LIMIT 3"
        all_members = execute_query(all_query)
        print(f"Last 3 members: {all_members}")
        
        # Delete the test member
        delete_query = "DELETE FROM team_members WHERE id = %s"
        deleted = execute_query(delete_query, (new_id,), fetch=False)
        print(f"Test member deleted: {deleted} rows affected")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
