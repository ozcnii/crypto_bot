from datetime import datetime, timedelta
from sqlalchemy import update
import pytz
import Database

Boosters = Database.Boosters

async def should_reset_boosters(last_reset, session, user_id):
  now = datetime.now(pytz.timezone('Europe/Moscow'))
  reset_interval = timedelta(hours=24)
  if now - last_reset >= reset_interval:
    await session.execute(
      update(Boosters).filter(Boosters.user_id == user_id).values({
				Boosters.turbo_range_uses: 3, Boosters.x_leverage_uses: 3, Boosters.last_reset: now
			}))
    await session.commit()
    return True
  return False