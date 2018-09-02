import React from 'react';
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types'
import Typography from '@material-ui/core/Typography';
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'
import TableCell from '@material-ui/core/TableCell'


class DataTable extends React.Component {
  _buildHeaderCell(fieldName) {
    fieldName = fieldName.charAt(0).toUpperCase() + fieldName.slice(1);
    fieldName = fieldName.match(/[A-Z][a-z]+/g).join(" ");
    return (
      <TableCell key={fieldName}>{fieldName}</TableCell>
    )
  }

  _buildHeader(headerFieldNames) {
    return (
      <TableRow>
        {headerFieldNames.map((fieldName) => (this._buildHeaderCell(fieldName)))}
      </TableRow>
    )
  }

  _buildCell(cellName, cellValue) {
    return (
        <TableCell key={cellName}>{cellValue}</TableCell>
    )
  }

  _buildTable(fieldNames) {
    return this.props.data.map((row) => (
      <TableRow>
        {fieldNames.map((fieldName) => (this._buildCell(fieldName, row[fieldName])))}
      </TableRow>
    ));
  }

  render() {
    let tableFieldNames = Object.keys(this.props.data[0]);
    //remove redundant element
    tableFieldNames.pop();
    if (this.props.data === null || this.props.data.length === 0) {
      return (<React.Fragment/>)
    }

    return (
      <Table>
        <TableHead>
          {this._buildHeader(tableFieldNames)}
        </TableHead>
        <TableBody>
          {this._buildTable(tableFieldNames)}
        </TableBody>
      </Table>
    )
  }
}

export default withStyles(styles)(DataTable);

DataTable.propTypes = {
  data: PropTypes.array.isRequired,
};