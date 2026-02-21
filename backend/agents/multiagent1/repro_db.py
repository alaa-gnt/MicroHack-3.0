import psycopg
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.base import Checkpoint, CheckpointMetadata, CheckpointTuple

DB_URI = "postgresql://postgres:password123@localhost:5432/micro_hack_db"

def test_checkpoint_saver():
    print("\nTesting PostgresSaver...")
    try:
        # Fix max_size to be >= min_size (default 4) or set min_size=1
        pool = ConnectionPool(conninfo=DB_URI, min_size=1, max_size=10, kwargs={"autocommit": True, "prepare_threshold": 0})
        checkpointer = PostgresSaver(pool)
        checkpointer.setup()
        print("✅ PostgresSaver setup successful.")

        # Simulate writing a checkpoint
        config = {"configurable": {"thread_id": "test_thread_repro"}}
        checkpoint = {
            "v": 1, 
            "ts": "2023-10-27T00:00:00Z", 
            "channel_values": {"key": "value"}, 
            "channel_versions": {"key": 1}, 
            "versions_seen": {}, 
            "pending_sends": [],
            "id": "test_checkpoint_id"
        }
        metadata = {"source": "test", "step": 1, "writes": {}, "parents": {}}
        
        # PostgresSaver.put(config, checkpoint, metadata, new_versions)
        # Note: Depending on langgraph version, signature might vary.
        # But let's try calling put()
        
        print("Attempting to write checkpoint...")
        checkpointer.put(config, checkpoint, metadata, {})
        print("✅ Checkpoint write successful.")

    except Exception as e:
        print(f"❌ PostgresSaver failed: {e}")

if __name__ == "__main__":
    test_checkpoint_saver()
