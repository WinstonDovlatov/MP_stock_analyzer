import './App.css';
import ReactSpeedometer from "react-d3-speedometer"
import React, { useState, useEffect } from 'react';


function App() {
  const [score, setScore] = useState(0);
  const [date_info, setDate] = useState("2024-04-17");

  useEffect(() => {
    fetch('http://localhost:12345')
      .then(response => response.json())
      .then(data => {
        setScore(data.score); 
        setDate(data.day);
      })
      .catch(error => {
        console.error('Ошибка при получении данных:', error);
      });
  }, []);


  return (
    <div>
      {/* Синяя секция */}
      <div className="blue-section">
        <h2 style={{ textAlign: 'center' }}>Оценка международной обстановки на фондовых рынках</h2>
        <p style={{ textAlign: 'center' }}>Проверьте, не пришел ли "черный лебедь"</p>
      </div>
      
      {/* Белая секция */}
      <div className="white-section">
        <div className="description">
          <h2>Ситуация на рынке сегодня стабильная</h2>
          <h3>Дата: {date_info}</h3>
          <p style={{ textAlign: 'center' }}>Наш метод не показал значительных отклонений в поведении бирж<br/>
          Сегодняшний день почти такой же, как и другие обычные дни<br/><br/><br/>Не является инвистиционной рекомендацией </p>
        </div>
        <div className="speedometer">
        <h3 style={{ textAlign: 'center' }}>Степень аномальности</h3>
        <ReactSpeedometer
           customSegmentStops={[0, 700, 900, 1000]}
           segmentColors={["limegreen", "gold", "tomato"]}
           value={score}
           textColor="black"
           />
        </div>
      </div>
    </div>
  );
}


export default App;
