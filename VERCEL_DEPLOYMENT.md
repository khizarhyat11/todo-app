# vercel deployment guide

## option 1: deploy using vercel cli (recommended)

### step 1: install vercel cli
```bash
npm install -g vercel
```

### step 2: deploy
navigate to your project directory and run:
```bash
cd "c:\Users\Tricle\Desktop\todo app-phase1"
vercel
```

### step 3: follow prompts
- login to your vercel account
- confirm project name
- select project root (current directory)
- skip creating vercel.json if asked (we already have one)

your api will be deployed and you'll get a live url.

---

## option 2: deploy using vercel web dashboard

### step 1: connect github
1. go to https://vercel.com/new
2. select "import project"
3. paste your github repo: https://github.com/khizarhyat11/todo-app
4. click "import"

### step 2: configure
- **framework preset**: select "other"
- **root directory**: leave default (.)
- **build command**: leave empty (vercel auto-detects)
- **output directory**: leave default

### step 3: deploy
click "deploy" button. vercel will:
1. clone your repo
2. install dependencies (requirements.txt)
3. build your api
4. deploy to serverless functions

---

## testing your deployment

once deployed, you'll get a url like: `https://todo-app-xxxxxx.vercel.app`

### test endpoints
```bash
# root endpoint
curl https://todo-app-xxxxxx.vercel.app/

# health check
curl https://todo-app-xxxxxx.vercel.app/health

# create a task
curl -x post https://todo-app-xxxxxx.vercel.app/tasks \
  -h "content-type: application/json" \
  -d '{"title":"buy milk","description":"whole milk"}'

# list tasks
curl https://todo-app-xxxxxx.vercel.app/tasks

# interactive docs
open https://todo-app-xxxxxx.vercel.app/docs
```

---

## api documentation

after deployment, visit:
- **swagger ui (interactive)**: https://todo-app-xxxxxx.vercel.app/docs
- **redoc (detailed)**: https://todo-app-xxxxxx.vercel.app/redoc

---

## important notes

### in-memory storage
⚠️ data is **not persisted** across deployments. each restart clears all tasks.

**to fix this for production:**
1. add a database (postgresql, mongodb, etc.)
2. update `store.py` to use database instead of memory
3. no changes needed to api endpoints

### environment variables
if needed later, set them in vercel dashboard:
1. project settings → environment variables
2. add your secrets
3. redeploy

### logs
view deployment logs:
```bash
vercel logs <deployment-url>
```

or visit: https://vercel.com → projects → select your project

---

## troubleshooting

### deployment fails
check vercel logs for errors:
```bash
vercel logs
```

common issues:
- missing `python` runtime (vercel auto-detects from requirements.txt)
- invalid python version (ensure 3.10+)

### api returns 500 error
1. check vercel logs
2. ensure `src/` folder is included in repo
3. verify imports in `api.py`

### cors errors
cors is already enabled in `api.py`. if you have issues:
- check browser console for actual error
- update allowed origins in `api.py` if needed

---

## next steps

1. ✅ deploy to vercel using cli or dashboard
2. 📝 test all endpoints at `/docs`
3. 💾 **phase-iii**: add database for persistence
4. 🔐 **phase-iv**: add authentication/authorization

---

## quick deployment checklist

- [ ] vercel account created
- [ ] vercel cli installed (or web dashboard ready)
- [ ] github repo pushed (already done)
- [ ] run `vercel` or click deploy button
- [ ] wait for deployment to complete
- [ ] test `/health` endpoint
- [ ] test `/docs` interactive documentation
- [ ] bookmark your deployment url

**deployed!** 🎉

