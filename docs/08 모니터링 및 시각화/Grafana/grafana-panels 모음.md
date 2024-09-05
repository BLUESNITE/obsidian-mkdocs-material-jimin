>[!TIP] 그라파나 그려둔 panels를 backup하기 위해 작성
>각각의 Json 내용이 길기 때문에 제목과 동일하게 하단에 Json 추가 작성

```json title:최근_사용자_활동
{
  "datasource": {
    "type": "prometheus",
    "uid": "cdqmf3aot7tvka"
  },
  "fieldConfig": {
    "defaults": {
      "mappings": [],
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {
            "color": "green",
            "value": null
          },
          {
            "color": "red",
            "value": 80
          }
        ]
      },
      "color": {
        "mode": "thresholds"
      }
    },
    "overrides": []
  },
  "gridPos": {
    "h": 8,
    "w": 12,
    "x": 0,
    "y": 1
  },
  "id": 10,
  "options": {
    "reduceOptions": {
      "values": false,
      "calcs": [
        "lastNotNull"
      ],
      "fields": ""
    },
    "orientation": "auto",
    "displayMode": "gradient",
    "valueMode": "color",
    "namePlacement": "auto",
    "showUnfilled": true,
    "sizing": "auto",
    "minVizWidth": 8,
    "minVizHeight": 16,
    "maxVizHeight": 300
  },
  "pluginVersion": "11.0.0",
  "targets": [
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(go_goroutines{job=\"vm-exporter\", instance=\"188.122.2.131:9100\"})",
      "instant": false,
      "legendFormat": "Node 01",
      "range": true,
      "refId": "A"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(go_goroutines{job=\"vm-exporter\", instance=\"188.122.2.132:9100\"})",
      "hide": false,
      "instant": false,
      "legendFormat": "Node 02",
      "range": true,
      "refId": "B"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(go_goroutines{job=\"vm-exporter\", instance=\"188.122.2.133:9100\"})",
      "hide": false,
      "instant": false,
      "legendFormat": "Node 03",
      "range": true,
      "refId": "C"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(go_goroutines{job=\"vm-exporter\", instance=\"188.122.2.134:9100\"})",
      "hide": false,
      "instant": false,
      "legendFormat": "Node 04",
      "range": true,
      "refId": "D"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(go_goroutines{job=\"vm-exporter\", instance=\"188.122.2.135:9100\"})",
      "hide": false,
      "instant": false,
      "legendFormat": "Node 05",
      "range": true,
      "refId": "E"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(go_goroutines{job=\"vm-exporter\", instance=\"188.122.2.136:9100\"})",
      "hide": false,
      "instant": false,
      "legendFormat": "Node 06",
      "range": true,
      "refId": "F"
    }
  ],
  "title": "최근 사용자 활동 (활성화된 Go 루틴 수)",
  "type": "bargauge"
}

```
![[Pasted image 20240708155246.png]]

```json title:현재_활성화된_Java_스레드_수
{
  "datasource": {
    "type": "prometheus",
    "uid": "cdqmf3aot7tvka"
  },
  "description": "",
  "fieldConfig": {
    "defaults": {
      "custom": {
        "drawStyle": "line",
        "lineInterpolation": "linear",
        "barAlignment": 0,
        "lineWidth": 1,
        "fillOpacity": 0,
        "gradientMode": "none",
        "spanNulls": false,
        "insertNulls": false,
        "showPoints": "auto",
        "pointSize": 5,
        "stacking": {
          "mode": "none",
          "group": "A"
        },
        "axisPlacement": "auto",
        "axisLabel": "",
        "axisColorMode": "text",
        "axisBorderShow": false,
        "scaleDistribution": {
          "type": "linear"
        },
        "axisCenteredZero": false,
        "hideFrom": {
          "tooltip": false,
          "viz": false,
          "legend": false
        },
        "thresholdsStyle": {
          "mode": "off"
        }
      },
      "color": {
        "mode": "palette-classic"
      },
      "mappings": [],
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {
            "color": "green",
            "value": null
          },
          {
            "color": "red",
            "value": 80
          }
        ]
      }
    },
    "overrides": []
  },
  "gridPos": {
    "h": 8,
    "w": 12,
    "x": 0,
    "y": 9
  },
  "id": 9,
  "options": {
    "tooltip": {
      "mode": "single",
      "sort": "none",
      "maxHeight": 600
    },
    "legend": {
      "showLegend": true,
      "displayMode": "list",
      "placement": "bottom",
      "calcs": []
    }
  },
  "targets": [
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "java_lang_Threading_ThreadCount{job=\"jmx-exporter\", instance=\"188.122.2.130:32397\"}",
      "instant": false,
      "legendFormat": "ABCDE-API-COMMON",
      "range": true,
      "refId": "A"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "java_lang_Threading_ThreadCount{job=\"jmx-exporter\", instance=\"188.122.2.130:31256\"}",
      "instant": false,
      "legendFormat": "ABCDE-API-MEMBER",
      "range": true,
      "refId": "B"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "java_lang_Threading_ThreadCount{job=\"jmx-exporter\", instance=\"188.122.2.130:30664\"}",
      "instant": false,
      "legendFormat": "ABCDE-API-EVENT",
      "range": true,
      "refId": "C"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "java_lang_Threading_ThreadCount{job=\"jmx-exporter\", instance=\"188.122.2.130:31633\"}",
      "instant": false,
      "legendFormat": "ABCDE-API-GOODS",
      "range": true,
      "refId": "D"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "java_lang_Threading_ThreadCount{job=\"jmx-exporter\", instance=\"188.122.2.130:30706\"}",
      "instant": false,
      "legendFormat": "ABCDE-API-DISPLAY",
      "range": true,
      "refId": "E"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "java_lang_Threading_ThreadCount{job=\"jmx-exporter\", instance=\"188.122.2.130:32218\"}",
      "instant": false,
      "legendFormat": "ABCDE-API-ORDER",
      "range": true,
      "refId": "F"
    }
  ],
  "title": "현재 활성화된 Java 스레드 수",
  "type": "timeseries"
}
```
![[Pasted image 20240708163547.png]]

```json title:쿠버네티스_워커노드_Virtual_Memory
{
  "datasource": {
    "type": "prometheus",
    "uid": "cdqmf3aot7tvka"
  },
  "description": "",
  "fieldConfig": {
    "defaults": {
      "custom": {
        "drawStyle": "line",
        "lineInterpolation": "linear",
        "barAlignment": 0,
        "lineWidth": 1,
        "fillOpacity": 0,
        "gradientMode": "none",
        "spanNulls": true,
        "insertNulls": false,
        "showPoints": "never",
        "pointSize": 5,
        "stacking": {
          "mode": "none",
          "group": "A"
        },
        "axisPlacement": "auto",
        "axisLabel": "",
        "axisColorMode": "text",
        "axisBorderShow": false,
        "scaleDistribution": {
          "type": "linear"
        },
        "axisCenteredZero": false,
        "hideFrom": {
          "tooltip": false,
          "viz": false,
          "legend": false
        },
        "thresholdsStyle": {
          "mode": "off"
        }
      },
      "color": {
        "mode": "palette-classic"
      },
      "mappings": [],
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {
            "color": "green",
            "value": null
          },
          {
            "color": "red",
            "value": 80
          }
        ]
      },
      "unit": "bytes"
    },
    "overrides": []
  },
  "gridPos": {
    "h": 8,
    "w": 12,
    "x": 0,
    "y": 17
  },
  "id": 7,
  "options": {
    "tooltip": {
      "mode": "single",
      "sort": "none",
      "maxHeight": 600
    },
    "legend": {
      "showLegend": true,
      "displayMode": "list",
      "placement": "bottom",
      "calcs": []
    }
  },
  "targets": [
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(process_resident_memory_bytes{job=\"vm-exporter\", instance=\"188.122.2.131:9100\"})",
      "instant": false,
      "legendFormat": "Node 01",
      "range": true,
      "refId": "A"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(process_resident_memory_bytes{job=\"vm-exporter\", instance=\"188.122.2.132:9100\"})",
      "hide": false,
      "instant": false,
      "legendFormat": "Node 02",
      "range": true,
      "refId": "B"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(process_resident_memory_bytes{job=\"vm-exporter\", instance=\"188.122.2.133:9100\"})",
      "hide": false,
      "instant": false,
      "legendFormat": "Node 03",
      "range": true,
      "refId": "C"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(process_resident_memory_bytes{job=\"vm-exporter\", instance=\"188.122.2.134:9100\"})",
      "hide": false,
      "instant": false,
      "legendFormat": "Node 04",
      "range": true,
      "refId": "D"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(process_resident_memory_bytes{job=\"vm-exporter\", instance=\"188.122.2.135:9100\"})",
      "hide": false,
      "instant": false,
      "legendFormat": "Node 05",
      "range": true,
      "refId": "E"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(process_resident_memory_bytes{job=\"vm-exporter\", instance=\"188.122.2.136:9100\"})",
      "hide": false,
      "instant": false,
      "legendFormat": "Node 06",
      "range": true,
      "refId": "F"
    }
  ],
  "title": "쿠버네티스 워커노드 Virtual Memory",
  "type": "timeseries"
}
```
![[Pasted image 20240708163604.png]]

```json title:어플리케이션_상태
{
  "datasource": {
    "type": "prometheus",
    "uid": "cdqmf3aot7tvka"
  },
  "fieldConfig": {
    "defaults": {
      "mappings": [],
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {
            "color": "green",
            "value": null
          },
          {
            "color": "red",
            "value": 80
          }
        ]
      },
      "color": {
        "mode": "thresholds"
      }
    },
    "overrides": []
  },
  "gridPos": {
    "h": 8,
    "w": 12,
    "x": 0,
    "y": 26
  },
  "id": 5,
  "options": {
    "reduceOptions": {
      "values": false,
      "calcs": [
        "lastNotNull"
      ],
      "fields": ""
    },
    "orientation": "horizontal",
    "textMode": "auto",
    "wideLayout": true,
    "colorMode": "value",
    "graphMode": "none",
    "justifyMode": "auto",
    "showPercentChange": false,
    "text": {
      "titleSize": 14,
      "valueSize": 14
    }
  },
  "pluginVersion": "11.0.0",
  "targets": [
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "exemplar": false,
      "expr": "up{job='jmx-exporter', instance=\"188.122.2.130:32397\"}",
      "instant": true,
      "legendFormat": "ABCDE-API-COMMON",
      "range": false,
      "refId": "A"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "exemplar": false,
      "expr": "up{job='jmx-exporter', instance=\"188.122.2.130:31256\"}",
      "hide": false,
      "instant": true,
      "legendFormat": "ABCDE-API-MEMBER",
      "range": false,
      "refId": "B"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "exemplar": false,
      "expr": "up{job='jmx-exporter', instance=\"188.122.2.130:30664\"}",
      "hide": false,
      "instant": true,
      "legendFormat": "ABCDE-API-EVENT",
      "range": false,
      "refId": "C"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "exemplar": false,
      "expr": "up{job='jmx-exporter', instance=\"188.122.2.130:31633\"}",
      "hide": false,
      "instant": true,
      "legendFormat": "ABCDE-API-GOODS",
      "range": false,
      "refId": "D"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "exemplar": false,
      "expr": "up{job='jmx-exporter', instance=\"188.122.2.130:30706\"}",
      "hide": false,
      "instant": true,
      "legendFormat": "ABCDE-API-DISPLAY",
      "range": false,
      "refId": "E"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "exemplar": false,
      "expr": "up{job='jmx-exporter', instance=\"188.122.2.130:32218\"}",
      "hide": false,
      "instant": true,
      "legendFormat": "ABCDE-API-ORDER",
      "range": false,
      "refId": "ORDER"
    }
  ],
  "title": "어플리케이션 상태",
  "type": "stat"
}
```
![[Pasted image 20240708163615.png]]

```json title:최근_5분간_쿠버네티스_워커노드_메모리_사용량
{
  "datasource": {
    "type": "prometheus",
    "uid": "cdqmf3aot7tvka"
  },
  "fieldConfig": {
    "defaults": {
      "custom": {
        "drawStyle": "line",
        "lineInterpolation": "linear",
        "barAlignment": 0,
        "lineWidth": 1,
        "fillOpacity": 0,
        "gradientMode": "none",
        "spanNulls": true,
        "insertNulls": false,
        "showPoints": "auto",
        "pointSize": 5,
        "stacking": {
          "mode": "none",
          "group": "A"
        },
        "axisPlacement": "left",
        "axisLabel": "",
        "axisColorMode": "text",
        "axisBorderShow": false,
        "scaleDistribution": {
          "type": "linear"
        },
        "axisCenteredZero": false,
        "hideFrom": {
          "tooltip": false,
          "viz": false,
          "legend": false
        },
        "thresholdsStyle": {
          "mode": "off"
        },
        "lineStyle": {
          "fill": "solid"
        }
      },
      "color": {
        "mode": "palette-classic"
      },
      "mappings": [],
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {
            "color": "green",
            "value": null
          },
          {
            "color": "red",
            "value": 80
          }
        ]
      },
      "unit": "bytes"
    },
    "overrides": []
  },
  "gridPos": {
    "h": 8,
    "w": 12,
    "x": 0,
    "y": 35
  },
  "id": 6,
  "options": {
    "tooltip": {
      "mode": "single",
      "sort": "none",
      "maxHeight": 600
    },
    "legend": {
      "showLegend": true,
      "displayMode": "list",
      "placement": "bottom",
      "calcs": []
    }
  },
  "targets": [
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "rate(process_cpu_seconds_total{job=\"vm-exporter\", instance=\"188.122.2.131:9100\"}[5m])",
      "instant": false,
      "legendFormat": "Kubernetes Worker Node 01",
      "range": true,
      "refId": "A"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "rate(process_cpu_seconds_total{job=\"vm-exporter\", instance=\"188.122.2.132:9100\"}[5m])",
      "hide": false,
      "instant": false,
      "legendFormat": "Kubernetes Worker Node 02",
      "range": true,
      "refId": "B"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "rate(process_cpu_seconds_total{job=\"vm-exporter\", instance=\"188.122.2.133:9100\"}[5m])",
      "hide": false,
      "instant": false,
      "legendFormat": "Kubernetes Worker Node 03",
      "range": true,
      "refId": "C"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "rate(process_cpu_seconds_total{job=\"vm-exporter\", instance=\"188.122.2.134:9100\"}[5m])",
      "hide": false,
      "instant": false,
      "legendFormat": "Kubernetes Worker Node 04",
      "range": true,
      "refId": "D"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "rate(process_cpu_seconds_total{job=\"vm-exporter\", instance=\"188.122.2.135:9100\"}[5m])",
      "hide": false,
      "instant": false,
      "legendFormat": "Kubernetes Worker Node 05",
      "range": true,
      "refId": "E"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "rate(process_cpu_seconds_total{job=\"vm-exporter\", instance=\"188.122.2.136:9100\"}[5m])",
      "hide": false,
      "instant": false,
      "legendFormat": "Kubernetes Worker Node 06",
      "range": true,
      "refId": "F"
    }
  ],
  "title": "최근 5분간 쿠버네티스 워커노드 메모리 사용량",
  "type": "timeseries"
}
```
![[Pasted image 20240708163628.png]]

```json title:최근_5분간_메모리사용량_어플리케이션
{
  "datasource": {
    "type": "prometheus",
    "uid": "cdqmf3aot7tvka"
  },
  "description": "jvm_memory_pool_used_bytes",
  "fieldConfig": {
    "defaults": {
      "custom": {
        "drawStyle": "line",
        "lineInterpolation": "linear",
        "barAlignment": 0,
        "lineWidth": 1,
        "fillOpacity": 0,
        "gradientMode": "none",
        "spanNulls": false,
        "insertNulls": false,
        "showPoints": "auto",
        "pointSize": 5,
        "stacking": {
          "mode": "none",
          "group": "A"
        },
        "axisPlacement": "left",
        "axisLabel": "",
        "axisColorMode": "text",
        "axisBorderShow": false,
        "scaleDistribution": {
          "type": "linear"
        },
        "axisCenteredZero": false,
        "hideFrom": {
          "tooltip": false,
          "viz": false,
          "legend": false
        },
        "thresholdsStyle": {
          "mode": "off"
        }
      },
      "color": {
        "mode": "palette-classic"
      },
      "mappings": [],
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {
            "color": "green",
            "value": null
          },
          {
            "color": "red",
            "value": 80
          }
        ]
      },
      "decimals": 0,
      "unit": "kbytes"
    },
    "overrides": []
  },
  "gridPos": {
    "h": 8,
    "w": 12,
    "x": 0,
    "y": 43
  },
  "id": 2,
  "options": {
    "tooltip": {
      "mode": "single",
      "sort": "none",
      "maxHeight": 600
    },
    "legend": {
      "showLegend": true,
      "displayMode": "list",
      "placement": "bottom",
      "calcs": []
    }
  },
  "targets": [
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(rate(jvm_memory_pool_used_bytes{job=\"jmx-exporter\", instance=\"188.122.2.130:32397\"}[$__rate_interval]))",
      "instant": false,
      "legendFormat": "ABCDE-API-COMMON",
      "range": true,
      "refId": "A"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(rate(jvm_memory_pool_used_bytes{job=\"jmx-exporter\", instance=\"188.122.2.130:31256\"}[$__rate_interval]))",
      "hide": false,
      "instant": false,
      "legendFormat": "ABCDE-API-MEMBER",
      "range": true,
      "refId": "B"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(rate(jvm_memory_pool_used_bytes{job=\"jmx-exporter\", instance=\"188.122.2.130:30664\"}[$__rate_interval]))",
      "hide": false,
      "instant": false,
      "legendFormat": "ABCDE-API-EVENT",
      "range": true,
      "refId": "C"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(rate(jvm_memory_pool_used_bytes{job=\"jmx-exporter\", instance=\"188.122.2.130:31633\"}[$__rate_interval]))",
      "hide": false,
      "instant": false,
      "legendFormat": "ABCDE-API-GOODS",
      "range": true,
      "refId": "D"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(rate(jvm_memory_pool_used_bytes{job=\"jmx-exporter\", instance=\"188.122.2.130:32218\"}[$__rate_interval]))",
      "hide": false,
      "instant": false,
      "legendFormat": "ABCDE-API-ORDER",
      "range": true,
      "refId": "E"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "sum(rate(jvm_memory_pool_used_bytes{job=\"jmx-exporter\", instance=\"188.122.2.130:30706\"}[$__rate_interval]))",
      "hide": false,
      "instant": false,
      "legendFormat": "ABCDE-API-DISPLAY",
      "range": true,
      "refId": "F"
    }
  ],
  "title": "최근 5분간 메모리사용량 - 어플리케이션",
  "type": "timeseries"
}
```
![[Pasted image 20240708163639.png]]

```json title:최근_5분간_CPU사용량_어플리케이션
{
  "datasource": {
    "type": "prometheus",
    "uid": "cdqmf3aot7tvka"
  },
  "description": "process_cpu_seconds_total",
  "fieldConfig": {
    "defaults": {
      "custom": {
        "drawStyle": "line",
        "lineInterpolation": "linear",
        "barAlignment": 0,
        "lineWidth": 1,
        "fillOpacity": 0,
        "gradientMode": "none",
        "spanNulls": false,
        "insertNulls": false,
        "showPoints": "auto",
        "pointSize": 5,
        "stacking": {
          "mode": "none",
          "group": "A"
        },
        "axisPlacement": "auto",
        "axisLabel": "",
        "axisColorMode": "text",
        "axisBorderShow": false,
        "scaleDistribution": {
          "type": "linear"
        },
        "axisCenteredZero": false,
        "hideFrom": {
          "tooltip": false,
          "viz": false,
          "legend": false
        },
        "thresholdsStyle": {
          "mode": "off"
        }
      },
      "color": {
        "mode": "palette-classic"
      },
      "mappings": [],
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {
            "color": "green",
            "value": null
          },
          {
            "color": "red",
            "value": 80
          }
        ]
      }
    },
    "overrides": []
  },
  "gridPos": {
    "h": 13,
    "w": 12,
    "x": 0,
    "y": 51
  },
  "id": 1,
  "options": {
    "tooltip": {
      "mode": "single",
      "sort": "none",
      "maxHeight": 600
    },
    "legend": {
      "showLegend": true,
      "displayMode": "list",
      "placement": "bottom",
      "calcs": []
    }
  },
  "targets": [
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "rate(process_cpu_seconds_total{job=\"jmx-exporter\", instance=\"188.122.2.130:32397\"}[5m])",
      "hide": false,
      "instant": false,
      "legendFormat": "ABCDE-API-COMMON",
      "range": true,
      "refId": "A"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "rate(process_cpu_seconds_total{job=\"jmx-exporter\", instance=\"188.122.2.130:31256\"}[5m])",
      "hide": false,
      "instant": false,
      "legendFormat": "ABCDE-API-MEMBER",
      "range": true,
      "refId": "B"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "rate(process_cpu_seconds_total{job=\"jmx-exporter\", instance=\"188.122.2.130:30664\"}[5m])",
      "hide": false,
      "instant": false,
      "legendFormat": "ABCDE-API-EVENT",
      "range": true,
      "refId": "C"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "rate(process_cpu_seconds_total{job=\"jmx-exporter\", instance=\"188.122.2.130:31633\"}[5m])",
      "hide": false,
      "instant": false,
      "legendFormat": "ABCDE-API-GOODS",
      "range": true,
      "refId": "D"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "rate(process_cpu_seconds_total{job=\"jmx-exporter\", instance=\"188.122.2.130:30706\"}[5m])",
      "hide": false,
      "instant": false,
      "legendFormat": "ABCDE-API-DISPLAY",
      "range": true,
      "refId": "E"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "cdqmf3aot7tvka"
      },
      "editorMode": "code",
      "expr": "rate(process_cpu_seconds_total{job=\"jmx-exporter\", instance=\"188.122.2.130:32218\"}[5m])",
      "hide": false,
      "instant": false,
      "legendFormat": "ABCDE-API-ORDER",
      "range": true,
      "refId": "G"
    }
  ],
  "title": "최근 5분간 CPU사용량 - 어플리케이션",
  "type": "timeseries"
}
```
![[Pasted image 20240708163653.png]]
___
