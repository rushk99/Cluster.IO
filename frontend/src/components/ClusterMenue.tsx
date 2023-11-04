import { gql, useQuery } from "@apollo/client";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  TextField,
} from "@mui/material";

import React, { useState } from "react";

type RenderOptionInputFieldProps = {
  name: string;
  type: string;
  description: string;
  setOptionValues: any;
  optionValues: any;
};

function RenderOptionInputField({
  name,
  type,
  description,
  setOptionValues,
  optionValues,
}: RenderOptionInputFieldProps) {
  switch (type) {
    case "INT":
      return (
        <TextField
          key={name}
          value={optionValues.name}
          label={name}
          onChange={(e) =>
            setOptionValues({
              ...optionValues,
              [name]: e.target.value,
            })
          }
        />
      );
    case "FLOAT":
      return (
        <TextField
          value={optionValues.name}
          label={name}
          onChange={(e) =>
            setOptionValues({
              ...optionValues,
              [name]: e.target.value,
            })
          }
        />
      );
    case "STRING":
      return (
        <TextField
          value={optionValues.name}
          label={name}
          onChange={(e) =>
            setOptionValues({
              ...optionValues,
              [name]: e.target.value,
            })
          }
        />
      );
    default:
      return <div>ERROR</div>;
  }
}

type ClusteringOptionsProps = {
  method: string;
  setOptionValues: any;
  optionValues: any;
};

function ClusteringOptions({
  method,
  setOptionValues,
  optionValues,
}: ClusteringOptionsProps) {
  const GET_OPTIONS_METHODS = gql`
    query method($method: String!) {
      clusteringMethod(name: $method) {
        options {
          name
          type
          description
        }
      }
    }
  `;

  const { loading, error, data } = useQuery(GET_OPTIONS_METHODS, {
    variables: { method },
  });

  let options =
    data &&
    data.clusteringMethod.options.map((v: any) => {
      return (
        <div key={v.name}>
          <RenderOptionInputField
            name={v.name}
            type={v.type}
            description={v.description}
            setOptionValues={setOptionValues}
            optionValues={optionValues}
          />
        </div>
      );
    });
  if (options) {
    return options;
  } else {
    return <div></div>;
  }
}

type ClusteringMethodProps = {
  clusteringMethod: string;
  setClusteringMethod: React.Dispatch<React.SetStateAction<string>>;
};

function ClusteringMethod({
  clusteringMethod,
  setClusteringMethod,
}: ClusteringMethodProps) {
  const GET_CLUSTERING_METHODS = gql`
    query {
      clusteringMethods {
        name
        label
      }
    }
  `;

  const { loading, error, data } = useQuery(GET_CLUSTERING_METHODS);
  return (
    <div>
      <InputLabel>Clustering Method</InputLabel>
      <Select
        value={clusteringMethod}
        onChange={(event) => {
          setClusteringMethod(event.target.value as string);
        }}
      >
        {loading ? (
          <MenuItem>Loading</MenuItem>
        ) : (
          data &&
          data.clusteringMethods.map((method: any) => (
            <MenuItem key={method.name} value={method.name}>
              {method.label}
            </MenuItem>
          ))
        )}
      </Select>
    </div>
  );
}

export default function ClusterMenue() {
  const [clusteringMethod, setClusteringMethod] = useState("");
  const [clusteringOptions, setClusteringOptions] = useState({});
  const [open, setOpen] = React.useState(false);

  return (
    <div>
      <Button variant="outlined" color="primary" onClick={() => setOpen(true)}>
        Create new cluster
      </Button>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Create new cluster</DialogTitle>
        <DialogContent>
          <ClusteringMethod
            setClusteringMethod={setClusteringMethod}
            clusteringMethod={clusteringMethod}
          />
          <ClusteringOptions
            method={clusteringMethod}
            optionValues={clusteringOptions}
            setOptionValues={setClusteringOptions}
          />
        </DialogContent>
        <DialogActions>
          <Button autoFocus onClick={() => setOpen(false)} color="primary">
            Cancel
          </Button>
          <Button onClick={() => setOpen(false)} color="primary">
            Cluster
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
