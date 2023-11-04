import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import { BrowserRouter as Router, Routes , Route } from 'react-router-dom';
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
      <Router>
      <Routes>
        <Route path="/*" element={ <App /> }>
        </Route>
      </Routes>
    </Router>
    </ApolloProvider>
  </React.StrictMode>,
  document.getElementById("root")
);



