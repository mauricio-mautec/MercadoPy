import React from 'react';
import classes from './Comando.module.css';
import Button from '../UI/Button/Button';

function comando (props) {
    return(
    <div className={classes.Comando}>
        <Button btnType="Alert" clicked={()=>{window.open("http://localhost:3000", "_blank")}}>NOVO PEDIDO</Button>&nbsp;
        <Button btnType="Alert" clicked={props.showInfoCliente}>CLIENTE</Button>
    </div>
    );
}

export default comando;