"""GraphQL routes."""

# Flask imports
from flask import Blueprint
from graphql_server.flask import GraphQLView

# Import GraphQL schema
from switchmap.server.db.schemas import SCHEMA

# Define the API_GRAPHQL global variable
API_GRAPHQL = Blueprint("API_GRAPHQL", __name__)

# Create the base GraphQL route
API_GRAPHQL.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql", schema=SCHEMA.graphql_schema, graphiql=False
    ),
)

# Create the base iGraphQL route
API_GRAPHQL.add_url_rule(
    "/igraphql",
    view_func=GraphQLView.as_view(
        "igraphql", schema=SCHEMA.graphql_schema, graphiql=True
    ),
)
