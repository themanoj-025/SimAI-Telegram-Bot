import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.K6_BASE_URL || 'http://localhost:8080';

export const options = {
  stages: [
    { duration: '30s', target: 10 },  // ramp up
    { duration: '1m', target: 10 },   // sustain
    { duration: '30s', target: 0 },   // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.05'],
  },
};

export default function () {
  // Health check
  const healthRes = http.get(`${BASE_URL}/health`);
  check(healthRes, {
    'health status is 200': (r) => r.status === 200,
    'health response time < 200ms': (r) => r.timings.duration < 200,
  });

  // Readiness check
  const readyRes = http.get(`${BASE_URL}/health/ready`);
  check(readyRes, {
    'ready status is 200': (r) => r.status === 200,
    'ready response time < 200ms': (r) => r.timings.duration < 200,
  });

  // Metrics endpoint
  const metricsRes = http.get(`${BASE_URL}/metrics`);
  check(metricsRes, {
    'metrics status is 200': (r) => r.status === 200,
    'metrics returns text': (r) => r.headers['Content-Type']?.includes('text/plain'),
  });

  // Root info
  const infoRes = http.get(`${BASE_URL}/`);
  check(infoRes, {
    'info status is 200': (r) => r.status === 200,
  });

  sleep(1);
}
