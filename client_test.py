import asyncio
import json
import sys
import hashlib
from dapr.actor import ActorProxy, ActorId
from datetime import datetime, timedelta, timezone

from scheduler.scheduler_actor_interface import SchedulerActorInterface

def generate_actor_id(message: str, timestamp_iso: str) -> str:
    raw = f"{message}-{timestamp_iso}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

async def main():
    message = sys.argv[1] if len(sys.argv) > 1 else "Hello World!"
    timestamp_iso = sys.argv[2] if len(sys.argv) > 2 else (datetime.now(timezone.utc) + timedelta(seconds=10)).isoformat()

    actor_id_str = generate_actor_id(message, timestamp_iso)
    actor_id = ActorId(actor_id_str)

    proxy = ActorProxy.create("SchedulerActor", actor_id, SchedulerActorInterface)
    await proxy.invoke_method("ScheduleMessage", json.dumps({
        "message": message,
        "scheduled_time_iso": timestamp_iso
    }).encode("utf-8"))

    print(f"[CLIENT] Scheduled message using actor ID: {actor_id_str}")

asyncio.run(main())
