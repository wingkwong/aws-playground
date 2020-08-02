# AppSync

- Schema-first Development
- No extra process for generating API documentation
- AppSync to GraphQL v.s. API Gateway to REST APIs

## Cognito Group-based Authorization

```graphql
schema {
   query: Query
   mutation: Mutation
}
```

```graphql
type Query {
   posts:[Post!]!
   @aws_auth(cognito_groups: ["Bloggers", "Readers"])
}

type Mutation {
   addPost(id:ID!, title:String!):Post!
   @aws_auth(cognito_groups: ["Bloggers"])
}
```

### Additional Authorization Modes

- ``@aws_api_key`` - To specify the field is API_KEY authorized.

- ``@aws_iam`` - To specify that the field is AWS_IAM authorized.

- ``@aws_oidc`` - To specify that the field is OPENID_CONNECT authorized.

- ``@aws_cognito_user_pools`` - To specify that the field is AMAZON_COGNITO_USER_POOLS authorized.

