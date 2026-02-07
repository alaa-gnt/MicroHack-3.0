import React, { useMemo } from "react";
import ReactECharts from "echarts-for-react";
import * as echarts from "echarts/core";
import { RadarChart as ERadarChart } from "echarts/charts";
import { RadarComponent, TooltipComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import "./TechnologyRadarChart.css";

echarts.use([ERadarChart, RadarComponent, TooltipComponent, CanvasRenderer]);

const TechnologyRadarChart = ({ data, loading }) => {
  const option = useMemo(() => {
    if (!data || data.length === 0) return {};

    const indicator = data.map((d) => ({
      name: d.name,
      max: 100,
    }));
    const values = data.map((d) => d.value);

    return {
      tooltip: {
        trigger: "item",
        backgroundColor: "#fff",
        borderColor: "#E5E7EB",
        borderWidth: 1,
        textStyle: {
          color: "#000",
          fontSize: 13,
          fontFamily: "Inter, sans-serif",
        },
      },
      radar: {
        shape: "circle",
        indicator: indicator,
        center: ["50%", "50%"],
        radius: "65%",
        startAngle: 90,
        splitNumber: 4,
        axisName: {
          color: "#333",
          fontSize: 12,
          fontWeight: 600,
          fontFamily: "Inter, sans-serif",
        },
        nameGap: 15,
        splitArea: {
          show: true,
          areaStyle: {
            color: [
              "rgba(245,245,247,0.3)",
              "rgba(230,230,230,0.1)",
            ],
          },
        },
        axisLine: {
          lineStyle: {
            color: "#888",
            width: 1,
          },
        },
        splitLine: {
          lineStyle: {
            color: "#ccc",
            width: 1,
          },
        },
      },
      series: [
        {
          type: "radar",
          data: [
            {
              value: values,
              name: "Technology Maturity (TRL)",
              symbol: "circle",
              symbolSize: 6,
              areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: "rgba(59, 130, 246, 0.5)" },
                  { offset: 1, color: "rgba(59, 130, 246, 0.1)" },
                ]),
              },
              lineStyle: {
                color: "#3B82F6",
                width: 2,
              },
              itemStyle: {
                color: "#3B82F6",
              },
            }
          ],
          emphasis: {
            lineStyle: { width: 3 },
          },
        },
      ],
      animation: true,
      animationDuration: 1000,
      animationEasing: "cubicOut",
    };
  }, [data]);

  if (loading) {
    return (
      <div className="radar-loading">
        <div className="radar-skeleton" />
      </div>
    );
  }

  return (
    <div className="radar-chart-wrapper">
      <ReactECharts
        option={option}
        style={{ height: "340px", width: "100%" }}
        notMerge={true}
        lazyUpdate={true}
      />
    </div>
  );
};

export default TechnologyRadarChart;
