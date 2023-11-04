import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import { ApolloClient, ApolloProvider, InMemoryCache,  } from "@apollo/client";
import createUploadLink from 'apollo-upload-client/createUploadLink.mjs';

const client = new ApolloClient({
  cache: new InMemoryCache(),
  uri: "http://127.0.0.1:8000/graphql/",
  link: createUploadLink({ uri: 'http://127.0.0.1:8000/graphql/' }),
});

ReactDOM.render(
  <React.StrictMode>
    <ApolloProvider client={client}>
      <App />
    </ApolloProvider>
  </React.StrictMode>,
  document.getElementById("root")
);



