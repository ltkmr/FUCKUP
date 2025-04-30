# init_chaos_node.py
# FUCKUP² Chaos Node Initializer

from oracle.qdrant_integration import ensure_collection

if __name__ == "__main__":
    print("🔮 Initializing Chaos Node (Qdrant collection)...")
    ensure_collection()
    print("✅ Collection 'divinations' ready.")
