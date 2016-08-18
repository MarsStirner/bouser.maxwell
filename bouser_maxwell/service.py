# -*- coding: utf-8 -*-
import json

import gtxamqp.pool
from twisted.application.service import Service
from twisted.internet import defer
from twisted.web import error
from twisted.web.resource import Resource

from bouser.helpers.api_helpers import get_json
from bouser.helpers.plugin_helpers import BouserPlugin, Dependency
from bouser.utils import api_method

__author__ = 'viruzzz-kun'


class BouserMaxwellService(Service, Resource, BouserPlugin):
    signal_name = 'bouser.maxwell'
    bouser = Dependency('bouser')
    web = Dependency('bouser.web')

    isLeaf = True

    def __init__(self, config):
        self.amqp_client = gtxamqp.pool.pool.get(config.get('amqp', {}))
        self.url_root = config.get('risar_url_root', 'http://localhost:6600/risar/api/integration/').rstrip('/')
        Service.__init__(self)
        Resource.__init__(self)

    @defer.inlineCallbacks
    @api_method
    def render(self, request):
        """
        Все ресурсы определяются здесь (можно вынести в отдельный фэйл). Сюда стучится РИСАР и пытается отдать данные
        в RabbitMQ.
        @type request: bouser.web.request.BouserRequest
        @param request:
        @return:
        """
        path = filter(None, request.postpath)
        if request.method != 'POST':
            # Разрешаем ходить только POST-ом
            defer.fail(error.UnsupportedMethod)

        if len(path) == 1 and path[0] == 'default':
            # Здесь должен быть разбор сообщения (тип сообщения, метаданные) и отправка его в RabbitMQ
            result = yield self.amqp_client.basic_publish(request.all_args)
            defer.returnValue(result)

    @defer.inlineCallbacks
    def on_amqp_message(self, msg):
        """
        Когда из очереди RabbitMQ валится сообщение, оно должно быть разобрано и отправлено в РИСАР.
        Урлы, на которые надо ходить в РИСАР, должны определяться здесь (можно вынести куда-то).
        @param msg:
        @return:
        """
        if msg and msg.content:
            content = json.loads(msg.content)
            # content здесь надо разобрать согласно формату сообщений (заголовки, вся фигня) и отдать в REST
            # То есть здесь должно быть много-много if-elif-else и много-много разных урлов
            result = yield get_json(self.url_root + '/1/echo', json=content, method='POST')
            defer.returnValue(result)

    @web.on
    def on_web(self, web):
        web.putChild('maxwell', self)

    @bouser.on
    def on_boot(self, _):
        self.amqp_client.basic_consume(self.on_amqp_message)
