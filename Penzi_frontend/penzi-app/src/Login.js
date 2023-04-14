import React from 'react'
import { Card, Container, Col, Row, Form, Button } from 'react-bootstrap'
import PenziIcon from './PenziIcon.jpg';
import { useEffect, useRef, useState } from 'react';
import { useUserContext } from './userContext';
import { useNavigate  } from 'react-router-dom';
import { type } from '@testing-library/user-event/dist/type';

const Login = ({setPhoneNumber}) => {
    const[phoneNumber, setPhoneNumberLocal]= useState('');
    const navigate = useNavigate();


    const handleLogin = (event) => {
        event.preventDefault();
        setPhoneNumber(phoneNumber);
        navigate('/chat');
        
    };
    

    // const handleOnChange = (event) => {
    //     setPhoneNumberLocal(event.target.value)
    // }

  return (
    <Container >
        <Row className='d-flex justify-content-center'>
            <Col md="8" lg="6" xl="4" style={{ position:'absolute', top:'50%',   transform: 'translateY(-50%)'}}>
            <Card className='mx-auto '>
                <Card.Header className='d-flex justify-content-center align-items-center' >
                <img src={PenziIcon} className='rounded-circle ' width={40} alt='penzi icon'></img>
                    <h6 className=' px-4' style={{color:'#0A1E80'}}>Welcome to PENZI  login </h6>
                </Card.Header>
                <Card.Body>
                    <Form onSubmit={handleLogin}>
                        <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Text className=" gap-3 pb-3" style={{paddingBottom:'2rem ', marginBottom:'10rem', color:'darkcyan', padding:'2rem !important'}}>
                            To get satrted you must login using your Phone Number
                        </Form.Text>
                            {/* <Form.Label className=''>Phone Number</Form.Label> */}
                            <Form.Control type="tel" placeholder="Enter phone number" value={phoneNumber} onChange={(event) => setPhoneNumberLocal(event.target.value)}/>
                        </Form.Group>
                        <Button variant="primary" type="submit" disabled={!phoneNumber}>
                            Login
                        </Button>
                    </Form>    
                </Card.Body>
            </Card>
            </Col>
        </Row>
    </Container>
  )
}

export default Login
