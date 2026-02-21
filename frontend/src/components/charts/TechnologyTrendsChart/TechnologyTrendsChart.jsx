import React, { useMemo } from "react";
import ReactECharts from "echarts-for-react";
import * as echarts from "echarts/core";
import { LineChart } from "echarts/charts";
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
} from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import "./TechnologyTrendsChart.css";

echarts.use([
  LineChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  CanvasRenderer,
]);

const TechnologyTrendsChart = ({ data, loading }) => {
  const option = useMemo(() => {
    if (!data || data.length === 0) return {};

    const weeks = data.map((d) => d.week);

    // Dynamically identify domains (keys other than 'week')
    const domains = Object.keys(data[0] || {}).filter(key => key !== 'week');

    const colors = ["#22C55E", "#EF4444", "#3B82F6", "#F59E0B", "#8B5CF6", "#EC4899"];

    const series = domains.map((domain, index) => ({
      name: domain.charAt(0).toUpperCase() + domain.slice(1),
      type: "line",
      data: data.map(d => d[domain] || 0),
      smooth: false,
      symbol: "circle",
      symbolSize: 8,
      lineStyle: {
        color: colors[index % colors.length],
        width: 2,
      },
      itemStyle: {
        color: colors[index % colors.length],
        borderColor: colors[index % colors.length],
        borderWidth: 2,
      },
      emphasis: {
        itemStyle: {
          borderWidth: 3,
          shadowBlur: 8,
          shadowColor: `${colors[index % colors.length]}4D`, // 30% opacity
        },
      },
    }));

    return {
      legend: {
        show: true,
        bottom: 0,
        textStyle: {
          fontFamily: "Inter, sans-serif",
          color: "#666"
        }
      },
      tooltip: {
        trigger: "axis",
        backgroundColor: "#fff",
        borderColor: "#E5E7EB",
        borderWidth: 1,
        textStyle: {
          color: "#000",
          fontSize: 13,
          fontFamily: "Inter, sans-serif",
        },
        axisPointer: {
          type: "cross",
          crossStyle: { color: "#ccc" },
        },
      },
      grid: {
        left: 50,
        right: 30,
        top: 20,
        bottom: 40,
        containLabel: false,
      },
      xAxis: {
        type: "category",
        data: weeks,
        boundaryGap: false,
        axisLine: {
          lineStyle: { color: "#333", width: 1.5 },
        },
        axisTick: { show: false },
        axisLabel: {
          color: "#666",
          fontSize: 12,
          fontFamily: "Inter, sans-serif",
          margin: 12,
        },
        splitLine: {
          show: true,
          lineStyle: { color: "#E8E8E8", type: "solid", width: 0.8 },
        },
      },
      yAxis: {
        type: "value",
        min: 0,
        max: 100,
        interval: 25,
        axisLine: {
          show: true,
          lineStyle: { color: "#333", width: 1.5 },
        },
        axisTick: { show: false },
        axisLabel: {
          color: "#666",
          fontSize: 12,
          fontFamily: "Inter, sans-serif",
          formatter: "{value}%",
        },
        splitLine: {
          show: true,
          lineStyle: { color: "#E8E8E8", type: "solid", width: 0.8 },
        },
      },
      series: series,
      animation: true,
      animationDuration: 800,
      animationEasing: "cubicOut",
    };
  }, [data]);

  if (loading) {
    return (
      <div className="chart-loading">
        <div className="chart-skeleton" />
      </div>
    );
  }

  return (
    <div className="trends-chart-wrapper">
      <ReactECharts
        option={option}
        style={{ height: "320px", width: "100%" }}
        notMerge={true}
        lazyUpdate={true}
      />
    </div>
  );
};

export default TechnologyTrendsChart;
