# ⚡ Quick Start Guide

Get the Weather Alert App running in under 5 minutes!

## Choose Your Path

### Option 1: Local Development (Docker)
**Best for:** Testing locally before deploying

1. **Prerequisites Check**
   ```bash
   docker --version
   docker-compose --version
   ```

2. **Clone & Configure**
   ```bash
   git clone https://github.com/marconn01/Weather_App.git
   cd Weather_App
   cp .env.example .env
   ```

3. **Add API Key**
   Edit `.env` and replace:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```
   Get free key at: https://openweathermap.org/api

4. **Run Application**
   ```bash
   docker-compose up -d
   ```

5. **Access Application**
   - Frontend: http://localhost:80
   - API: http://localhost:5000
   - Health: http://localhost:5000/health

---

### Option 2: AWS Deployment (Production)
**Best for:** Full cloud deployment

1. **Prerequisites**
   - AWS Account
   - AWS CLI configured
   - Terraform installed
   - OpenWeatherMap API key

2. **Quick Deploy**
   ```bash
   git clone https://github.com/marconn01/Weather_App.git
   cd Weather_App
   cp .env.example .env
   # Edit .env with your values
   
   cd scripts
   chmod +x project.sh
   ./project.sh
   ```

3. **Manual Deploy** (if script fails)
   
   See detailed guide: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 🧪 Verify Installation

### Test Backend
```bash
curl http://localhost:5000/health
# Expected: {"status": "ok"}

curl "http://localhost:5000/weather?city=London"
# Expected: JSON with weather data
```

### Test Frontend
Open browser to `http://localhost` and search for any city.

---

## View Logs

```bash
# All logs
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

---

## Stop Application

```bash
docker-compose down
```

---

## 🔧 Common Issues

### Issue: Port already in use
**Solution:**
```bash
# Change ports in .env
BACKEND_PORT=5001
FRONTEND_PORT=8080
```

### Issue: API returns 401 error
**Solution:** Check your API key in `.env` is correct

### Issue: Cannot connect to Docker
**Solution:**
```bash
sudo systemctl start docker
```

---

## Next Steps

1. Read [README.md](README.md) for full overview
2. Check [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) to understand the system
3. See [docs/API.md](docs/API.md) for API documentation
4. Review [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for AWS deployment

---

## Tips

- Use `docker-compose up --build` to rebuild after code changes
- Set `LOG_LEVEL=DEBUG` in `.env` for detailed logs
- Add popular cities to search history by using them once
- Check `backend/logs/app.log` for persistent logs

---

## More Docs

- Check [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for troubleshooting
- Open an issue on GitHub

---

**Ready to deploy? Let's go! 🚀**
