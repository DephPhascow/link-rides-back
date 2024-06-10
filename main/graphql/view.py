# -*- coding: utf-8 -*-

import os

import strawberry
from django.http import Http404, HttpRequest
from django.template import RequestContext, Template
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from strawberry.django.views import AsyncGraphQLView as StrawberryGraphQLView
from asgiref.sync import async_to_sync
from .context import Context, get_broadcast
from strawberry.django.views import GraphQLView

# class GraphQLView(StrawberryGraphQLView):
class GraphQLView(GraphQLView):
    def get_context(self, request: HttpRequest, response) -> Context:
        broadcast = async_to_sync(get_broadcast)()

        return Context(broadcast, request)

    # def _render_graphiql(self, request: HttpRequest, context=None):
    #     # if not self.graphiql:
    #     #     raise Http404()

    #     # try:
    #     #     template = Template(render_to_string("graphql/graphiql.html"))
    #     # except TemplateDoesNotExist:
    #     #     template = Template(
    #     #         open(
    #     #             os.path.join(
    #     #                 os.path.dirname(os.path.abspath(strawberry.__file__)),
    #     #                 "static/graphiql.html",
    #     #             ),
    #     #             "r",
    #     #         ).read()
    #     #     )

    #     context = context or {}
    #     # THIS enables subscriptions
    #     context.update({"SUBSCRIPTION_ENABLED": "true"})

    #     response = TemplateResponse(request=request, template=None, context=context)
    #     # response.content = template.render(RequestContext(request, context))
    #     return response