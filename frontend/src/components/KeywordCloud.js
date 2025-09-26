
'use client';

import { TagCloud } from 'react-tagcloud';
import { useMemo } from 'react';

const processDataForCloud = (data) => {
  if (!data || data.length === 0) {
    return [];
  }
  const wordCounts = {};
  data.forEach(comment => {
    comment.keywords.forEach(keyword => {
      wordCounts[keyword] = (wordCounts[keyword] || 0) + 1;
    });
  });


  return Object.keys(wordCounts).map(key => ({
    value: key,
    count: wordCounts[key],
  }));
};

export default function KeywordCloud({ data }) {
  const words = useMemo(() => processDataForCloud(data), [data]);

  const options = {
    luminosity: 'dark',
    hue: 'blue',
  };

  if (words.length === 0) {
    return <p>Not enough keyword data to display a cloud.</p>;
  }

  return (
    <div>
      <h3>Top Keywords</h3>
      <TagCloud
        minSize={12}
        maxSize={35}
        tags={words}
        colorOptions={options}
        onClick={tag => alert(`'${tag.value}' appeared ${tag.count} times`)}
      />
    </div>
  );
}