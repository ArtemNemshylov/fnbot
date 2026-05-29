import asyncio
import logging

from database.db_manipulations import UsersDB
from api.fn_api import get_fn_user_stats_raw, today_kyiv

log = logging.getLogger(__name__)


async def take_daily_snapshots():
    db = UsersDB()
    today = today_kyiv()
    users = db.get_all_users()

    success = 0
    for user_id, username in users:
        try:
            result = await asyncio.to_thread(get_fn_user_stats_raw, username)
            if result:
                stats, account_type = result
                db.save_daily_snapshot(
                    user_id, today,
                    stats['kills'], stats['deaths'], stats['wins'],
                    stats['matches'], stats['minutes'],
                    account_type
                )
                success += 1
        except Exception as e:
            log.error(f"Snapshot failed for {username}: {e}")

    log.info(f"Daily snapshots: {success}/{len(users)} users saved for {today}")
