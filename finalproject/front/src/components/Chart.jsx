import React, { useEffect, useState } from 'react'
import { Button, ButtonGroup, ButtonToolbar, Form, InputGroup, ToggleButton, ToggleButtonGroup } from 'react-bootstrap'
import { Line, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, registerables } from 'chart.js'
import 'chart.js/auto';
import axios from "axios"

ChartJS.register(...registerables)

const API_URL = 'http://localhost:20246/v1/'

const client = axios.create({
  baseURL: API_URL
})

const options = {
  scales: {
    x: {
      type: 'category',
      title: {
        display: true,
        text: '날짜',
      },
    },
    'y-axis-1': {
      type: 'linear',
      position: 'left',
      title: {
        display: true,
        text: '가격',
        
      },
      min: 0,
      ticks: {
        stepSize: 100000,
      },
    },
    'y-axis-2': {
      type: 'linear',
      position: 'right',
      title: {
        display: true,
        text: '판매량',
      },
      grid: {
        drawOnChartArea: false, // 오른쪽 Y축에 대한 그리드를 표시하지 않음
      },
      ticks: {
        stepSize: 10,
      }
    },
  },
};

export default function Chart({ item }) {
  const [interval, setInterval] = useState('day');
  const [storage, setStorage] = useState('');
  const [status, setStatus] = useState(true);
  const [battery, setBattery] = useState(0);
  const [featureList, setFeatureList] = useState([]);
  const [data, setData] = useState({})
  const periods = ['year', 'month', 'day']
  const storages = ['128GB', '256GB', '512GB', '1024GB']
  const features = ['기스', '찍힘', '흠집', '파손', '잔상', '미개봉', '애플케어플러스']

  const fetchData = async () => {
    try {
      let endpoint = `/joongos/${interval}?model=${item}` + (Boolean(battery) ? `&battery=${battery}` : '') + (Boolean(storage) ? `&featureList[0]=${storage}` : '') + ((status) ? `&status=1` : `&status=0`)
      featureList.forEach((feature, idx) => endpoint = endpoint + `&featureList[${idx+2}]=${feature}`)
      console.log(endpoint)
      console.log(featureList);
      console.log(featureList.includes('기스'));
      const res = await client.get(endpoint)
      const rawData = res.data
      rawData.sort((a, b) => new Date(a.date) - new Date(b.date));
      const dates = rawData.map(item => item.date);
      const prices = rawData.map(item => item.averagePrice);
      const counts = rawData.map(item => item.count);

      const data = {
        labels: dates,
        datasets: [
          {
            label: '가격',
            data: prices,
            type: 'line',
            fill: false,
            borderColor: 'rgba(75,192,192,1)',
            tension: 0.1,
            yAxisID: 'y-axis-1',
        },
        {
          label: '거래량',
          data: counts,
          type: 'bar',
          backgroundColor: 'rgba(153,102,255,0.5)',
          borderColor: 'rgba(153,102,255,1)',
          yAxisID: 'y-axis-2',
        }
        ]
      }
      
      setData(prev => data)
    } catch(err) {
      console.log(err);
    }
  }

  const handleStorage = (e) => {
    if(storage === e.currentTarget.value){
      setStorage('')
    }
    else {
      setStorage(e.currentTarget.value)
    }
  }

  const handleStatus = (e) => {
    setStatus(!status)
  }

  const handleBattery = (e) => {
    const input = e.target.value;
    if (!isNaN(input) && input >= 0 && input <= 100) {
      setBattery(input);
    } else if (input === '') {
      // 빈 문자열인 경우 (즉, 입력 필드를 비운 경우)
      setBattery(0);
    }
  }

  const handleFeature = (e) => {
    const feature = e.target.value
    if (featureList.includes(feature)) {
      setFeatureList(prev => prev.filter((elem) => elem !== feature))
    }
    else {
      setFeatureList(prev => [...prev, feature])
    }
  }

  useEffect(() => {
    fetchData();
  }, [interval, storage, status, battery, featureList])
  
  return (
    <>
      <ButtonToolbar className='d-flex justify-content-around'>
        <ButtonGroup>
          {periods.map((period, idx) => (
            <Button 
              variant={period === interval ? `primary` : `light`}
              value={period}
              onClick={(e) => setInterval(e.currentTarget.value)}>{period}</Button>
          ))}
        </ButtonGroup>
        <ButtonGroup>
          {storages.map((size) => (
            <Button
              variant={size === storage ? 'primary' : 'light'}
              value={size}
              onClick={handleStorage}
              >{size}</Button>
          ))}
        </ButtonGroup>
        <InputGroup
          variant='primary'>
          <InputGroup.Text>배터리</InputGroup.Text>
          <Form.Control
            className=''
            type='text'
            value={battery}
            onChange={handleBattery}
            style={{ textAlign: 'right' }}
            min="0"
            max="100"/>
          <InputGroup.Text id="basic-addon2">% 이상</InputGroup.Text>
        </InputGroup>
        <ButtonGroup>
          <Button 
            variant={status ? 'primary' : 'light'}
            onClick={handleStatus}
            >판매중</Button>
          <Button 
            variant={status ? 'light' : 'primary'}
            onClick={handleStatus}
            >판매완료</Button>
        </ButtonGroup>
        <ButtonGroup>
          {features.map((feature) => (
            <Button
              variant={featureList.includes(feature) ? 'primary' : 'light'}
              value={feature}
              onClick={handleFeature}
              >{feature}</Button>
          ))}
        </ButtonGroup>
      </ButtonToolbar>
      {Object.keys(data).length !== 0  && <Line data={data} options={options} />}
    </>
  )
}
