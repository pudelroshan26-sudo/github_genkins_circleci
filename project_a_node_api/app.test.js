const request = require('supertest');
const app = require('./app');

describe('REST API Endpoints', () => {
  test('GET /api/health returns status UP', async () => {
    const res = await request(app).get('/api/health');
    expect(res.statusCode).toEqual(200);
    expect(res.body).toHaveProperty('status', 'UP');
  });

  test('GET /api/users returns a list of users', async () => {
    const res = await request(app).get('/api/users');
    expect(res.statusCode).toEqual(200);
    expect(Array.isArray(res.body)).toBe(true);
    expect(res.body.length).toBe(3);
    expect(res.body[0].name).toEqual('Roshan Poudel');
  });

  test('POST /api/echo echoes back message', async () => {
    const res = await request(app)
      .post('/api/echo')
      .send({ message: 'Hello CI/CD!' });
    expect(res.statusCode).toEqual(200);
    expect(res.body).toHaveProperty('message', 'Hello CI/CD!');
  });

  test('POST /api/echo returns 400 when message is missing', async () => {
    const res = await request(app)
      .post('/api/echo')
      .send({});
    expect(res.statusCode).toEqual(400);
    expect(res.body).toHaveProperty('error', 'Message is required');
  });
});
