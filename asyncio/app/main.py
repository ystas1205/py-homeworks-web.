import asyncio
import aiohttp
import datetime
from more_itertools import chunked

from models import init_db, Session, SwapiPeople

MAX_CHUNK = 5


async def get_person(person_id, session):
    list_films = []
    list_species = []
    list_starships = []
    list_vehicles = []
    http_response = await session.get(
        f"https://swapi.py4e.com/api/people/{person_id}/")
    json_data = await http_response.json()
    for key, value in json_data.items():
        if (key == 'films' or key == 'species'
                or key == 'starships' or key == 'vehicles'):
            for get in value:
                response_http = await session.get(f"{get}")
                data = await response_http.json()
                if key == 'films':
                    list_films.append(data.get('title'))
                    json_data.update({'films': list_films})
                if key == 'species':
                    list_species.append(data.get('name'))
                    json_data.update({'species': list_species})
                if key == 'starships':
                    list_starships.append(data.get('name'))
                    json_data.update({'starships': list_starships})
                if key == 'vehicles':
                    list_vehicles.append(data.get('name'))
                    json_data.update({'vehicles': list_vehicles})
    return json_data


async def insert_records(records):
    list_swapi = []
    for record in records:
        if record == {'detail': 'Not found'}:
            continue
        data = SwapiPeople(name=record['name'],
                           birth_year=record['birth_year'],
                           eye_color=record['eye_color'],
                           films=','.join(record['films']),
                           gender=record['gender'],
                           hair_color=record['hair_color'],
                           height=record['height'],
                           homeworld=record['homeworld'],
                           mass=record['mass'],
                           skin_color=record['skin_color'],
                           species=','.join(record['species']),
                           starships=','.join(record['starships']),
                           vehicles=','.join(record['vehicles']))
        list_swapi.append(data)
    async with Session() as session:
        session.add_all(list_swapi)
        await session.commit()


async def main():
    await init_db()
    session = aiohttp.ClientSession()
    for people_id_chunk in chunked(range(1, 90), MAX_CHUNK):
        coros = [get_person(person_id, session) for person_id in
                 people_id_chunk]
        result = await asyncio.gather(*coros)
        asyncio.create_task(insert_records(result))

    await session.close()
    all_tasks_set = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*all_tasks_set)
    # for task in all_tasks_set:
    #     await task


if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
