#!/usr/bin/env python
# -*- coding: utf-8 -*-

from graphene import (
    Boolean, Field, ID, Int, List, Mutation, ObjectType, Schema, String)
from graphql.execution.executors.asyncio import AsyncioExecutor
from sanic import Sanic
from sanic_graphql import GraphQLView
from signal import signal, SIGINT

import asyncio
import logging
import sys
import uvloop


app = Sanic()

# resources
authors = dict()
comments = dict()
posts = dict()


class Author(ObjectType):

    id = ID()
    name = String(required=True)


class Comment(ObjectType):

    id = ID()
    author = Field(Author, required=True)
    text = String(required=True)


class Post(ObjectType):

    id = ID()
    author = Field(Author, required=True)
    text = String(required=True)
    comments = List(Comment)


class AddComment(Mutation):

    class Arguments:

        post_id = Int()
        author_id = Int()
        text = String()

    ok = Boolean()
    comment = Field(Comment)

    def mutate(self, info, post_id, author_id, text):
        author = authors[author_id]
        cmt = Comment(
            id=max([i for i in comments.keys()]) + 1,
            author=author,
            text=text)
        comments[cmt.id] = cmt

        post = posts[post_id]
        post.comments.append(cmt)

        return AddComment(ok=True, comment=cmt)


class MyRootQuery(ObjectType):

    newsfeed = List(Post)
    post = Field(Post, id=Int())

    def resolve_newsfeed(self, info):
        return posts.values()

    def resolve_post(self, info, id):
        return posts.get(id, None)


class MyRootMutation(ObjectType):

    add_comment = AddComment.Field()


@app.listener("before_server_start")
async def setup_data(app, loop):
    chester = Author(id=46, name="chester")
    ming = Author(id=0, name="ming")
    dainese = Author(id=74, name="DAiNESE")
    authors.update(dict((a.id, a) for a in [chester, ming, dainese]))

    cmt0 = Comment(id=0, author=ming, text="Good!")
    cmt1 = Comment(id=1, author=dainese, text="Awesome!")
    comments.update(dict((c.id, c) for c in [cmt0, cmt1]))

    post0 = Post(
        id=0, author=chester,
        text="Hello world")
    post1 = Post(
        id=1, author=chester,
        text="It's Graphs All the way Down!",
        comments=[cmt0, cmt1])
    posts.update(dict((p.id, p) for p in [post0, post1]))


if __name__ == "__main__":
    asyncio.set_event_loop(uvloop.new_event_loop())
    loop = asyncio.get_event_loop()

    graphql_view = GraphQLView.as_view(
        schema=Schema(query=MyRootQuery, mutation=MyRootMutation),
        executor=AsyncioExecutor(loop=loop))
    app.add_route(graphql_view, "/graphql", methods=["POST"])

    server = app.create_server(host="0.0.0.0", port=9487, debug=True)
    task = asyncio.ensure_future(server)
    signal(SIGINT, lambda s, f: loop.stop())

    try:
        loop.run_forever()
    except Exception:
        loop.stop()
