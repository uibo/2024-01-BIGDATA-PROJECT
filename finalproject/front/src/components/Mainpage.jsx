import React from 'react'
import { Accordion } from 'react-bootstrap'
import styled from 'styled-components'
import Chart from './Chart'

export default function Mainpage() {
  const items = ['iPhone14', 'iPhone14Plus', 'iPhone14Pro', 'iPhone14ProMax']

  return (
    <MainContainert>
      {items.map((item, idx) => {
        return(
        <Accordion defaultActiveKey={idx}>
          <Accordion.Item eventKey='1'>
            <Accordion.Header>{item}</Accordion.Header>
            <Accordion.Body><Chart item={item}></Chart></Accordion.Body>
          </Accordion.Item>
        </Accordion>
        )
      })}
  </MainContainert>
  )
}

const MainContainert = styled.div`
  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: column;
`
