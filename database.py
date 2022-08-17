from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlmodel.sql.expression import Select, SelectOfScalar
from typing import Optional
import json

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

class OutputChannel(SQLModel, table=True):
  id: Optional[int] = Field(primary_key=True, default=None)
  guild_id: int
  channel_id: int
  channel_type: str


class Database:
  def __init__(self) -> None:
    self.db_uri = "sqlite:///data/servers.db"
    self.engine = create_engine(self.db_uri)

  @property
  def session(self) -> Session:
    return Session(self.engine)

  def add_channel(self, channel: OutputChannel):
    with self.session as session:
      session.add(channel)
      session.commit()

  def fetch_channels(self):
    with self.session as session:
      ch = session.exec(select(OutputChannel)).all()
    return ch

  def delete_channel(self, id: int):
    with self.session as session:
      ch = session.exec(select(OutputChannel).where(OutputChannel.id == id)).first()
      session.delete(ch)
      session.commit()
    
  def get_channel_by_type(self, ch_type: str):
    with self.session as session:
      ch = session.exec(select(OutputChannel).where(OutputChannel.channel_type == ch_type)).all()
    return ch

  def validate_channel(self, channel_id: int):
    with self.session as session:
      channel = session.exec(select(OutputChannel).where(OutputChannel.channel_id == channel_id)).first()
    return True if not channel else False

  def add_input_channel(self, channel_id: int):
    with open("data/channels.json", "r") as f:
      data = json.load(f)
    if str(channel_id) in data["channels"]:
      return False
    data["channels"].append(str(channel_id))
    with open("data/channels.json", "w") as f:
      json.dump(data, f)
    return True

  def check_input_channel(self, channel_id: int):
    with open("data/channels.json", "r") as f:
      data = json.load(f)
    if str(channel_id) in data["channels"]:
      return True
    else:
      return False

if __name__ == '__main__':
    # Run this file to create a new table
    SQLModel.metadata.create_all(Database().engine)

  