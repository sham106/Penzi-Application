import React from 'react'
import { Container, Navbar, Form, Button, Table, Nav } from 'react-bootstrap';
import {RxDoubleArrowRight} from 'react-icons/rx'

const Admin = () => {
  return (
    <>
    <Navbar bg='dark' className='shadow'>
        <Container>
            <Navbar.Brand style={{color:'white', fontFamily:'cursive'}}>
                <span style={{color:'gold'}}>Penzi</span> Admin Page
            </Navbar.Brand>
            <Form className="d-flex" style={{border:'0px'}}>
                  <Form.Control
                    type="search"
                    placeholder="Search"
                    className="me-2"
                    aria-label="Search"
                  />
                  <Button variant="outline-success">Search</Button>
                </Form>
        </Container>
    </Navbar>
    {/* <Container className='mt-2'>
        
    <Table striped bordered hover >
      <thead>
        <tr>
          <th>User ID</th>
          <th>Name</th>
          <th>Phone Number</th>
          <th>MessageSent</th>
          <th>MessageReceived</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>1</td>
          <td>Mark</td>
          <td>Otto</td>
          <td>@mdo</td>
        </tr>
      </tbody>
    </Table>
            
    </Container> */}
    <Nav defaultActiveKey="/" className="flex-column  mt-1 shadow-md" 
    style={{width:'fit-content', height:'100vh',
    color:'white',
    alignItems:'center',
    borderTop:'3rem',
    backgroundColor:'maroon',
    display:'flex'
    }}>
        <div  style={{width:'100%', borderRadius:'20px',  }}>
            <Nav.Item style={{paddingLeft:'10px'}}>Users <span className='pl-4' style={{paddingLeft:'10px', justifyContent:'end'}}><RxDoubleArrowRight/></span></Nav.Item>
      </div>
      <br />
      <div  style={{width:'100%', borderRadius:'20px', }}>
            <Nav.Item style={{paddingLeft:'10px'}}>Details<span className='pl-4' style={{paddingLeft:'10px'}}><RxDoubleArrowRight/></span></Nav.Item>
      </div>
      <br/>
      <div  style={{width:'100%', borderRadius:'20px', }}>
            <Nav.Item style={{paddingLeft:'10px'}}>Description<span className='pl-4' style={{paddingLeft:'10px'}}><RxDoubleArrowRight/></span></Nav.Item>
      </div>
      <br/>
      <div  style={{width:'100%', borderRadius:'20px', }}>
            <Nav.Item style={{paddingLeft:'10px'}}>Messages<span className='pl-4' style={{paddingLeft:'10px'}}><RxDoubleArrowRight/></span></Nav.Item>
      </div>

    </Nav>
    
    </>
  )
}

export default Admin
