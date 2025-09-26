'use client';

import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';


const COLORS = {
  POSITIVE: '#7982B9', 
  NEGATIVE: '#A5C1DC', 
};

export default function SentimentChart({ data }) {
  if (!data || data.length === 0) {
    return <p>No data to display.</p>;
  }

 
  const positiveCount = data.filter(comment => comment.sentiment_label === 'POSITIVE').length;
  const negativeCount = data.length - positiveCount;


  const chartData = [
    { name: 'Positive', value: positiveCount },
    { name: 'Negative', value: negativeCount },
  ];

  return (

    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={chartData}
          cx="50%" 
          cy="50%" 
          labelLine={false}
          outerRadius={100}
          fill="#8884d8"
          dataKey="value" 
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
        >
          
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[entry.name.toUpperCase()]} />
          ))}
        </Pie>

        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  );
}