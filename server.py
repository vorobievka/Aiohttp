from aiohttp import web
from models import Session, Advert, engine, Base
from sqlalchemy.ext.asyncio import AsyncSession
import json
from sqlalchemy.exc import IntegrityError


app = web.Application()


async def orm_context(app):
    print('START')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print('FINISH')

app.cleanup_ctx.append(orm_context)


def get_http_error(error_class, message):
    response = json.dumps({'error': message})
    http_error = error_class(text=response, content_type='application/json')
    return http_error


async def get_advert_by_id(session, advert_id):
    advert = await session.get(Advert, advert_id)
    if advert is None:
        raise get_http_error(web.HTTPNotFound, f'Advert with id {advert_id} not found')
    return advert


async def add_advert(session, advert):
    try:
        session.add(advert)
        await session.commit()
    except IntegrityError:
        raise get_http_error(web.HTTPConflict, f'Advert with title {advert.title} already exist')


@web.middleware
async def session_middleware(request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


app.middlewares.append(session_middleware)


class AdvertView(web.View):

    @property
    def advert_id(self):
        return int(self.request.match_info['advert_id'])

    @property
    def session(self) -> AsyncSession:
        return self.request.session

    async def get_advert(self):
        advert = await get_advert_by_id(self.session, self.advert_id)
        return advert

    async def get(self):
        advert = await self.get_advert()
        return web.json_response(advert.dict)

    async def post(self):
        json_data = await self.request.json()
        advert = Advert(**json_data)
        await add_advert(self.session, advert)
        return web.json_response({
            'id': advert.id,
        })

    async def delete(self):
        advert = await self.get_advert()
        await self.session.delete(advert)
        await self.session.commit()
        return web.json_response({'status': 'deleted'})


app.add_routes(
    [web.get('/advert/{advert_id:\d+}', AdvertView),
     web.post('/advert', AdvertView),
     web.delete('/advert/{advert_id:\d+}', AdvertView)
     ]
)

web.run_app(app)
