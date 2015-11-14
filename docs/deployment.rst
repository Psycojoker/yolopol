Deployment on OpenShift
~~~~~~~~~~~~~~~~~~~~~~~

OpenShift is an Open-Source Platform-as-a-Service software by Red Hat. It is
also available in its hosted version known as "OpenShift Online" and the first
three websites ("gears") are free.

To deploy the website, use a command like::

    $ rhc app-create \
        python-2.7 \
        "http://cartreflect-claytondev.rhcloud.com/reflect?github=smarterclayton/openshift-redis-cart" \
        cron-1.4 \
        postgresql-9.2 \
        -n yourdomain \
        -a yourappname \
        -e DJANGO_SECRET_KEY=$(openssl rand -base64 32) \
        -e OPENSHIFT_PYTHON_WSGI_APPLICATION=memopol/wsgi.py \
        --from-code https://github.com/political-memory/political_memory.git
        --no-git

This should deploy the website. Add the git remote openshift created for you,
you can see it with ``rhc app-show``, ie.::

    $ rhc app-show -a yourappname
    [snip]
    Git URL:         ssh://569f5cf500045f6a1839a0a4@yourappname-yourdomain.rhcloud.com/~/git/yourappname.git/
    Initial Git URL: https://github.com/political-memory/political_memory.git
    SSH:             569f5cf500045f6a1839a0a4@yourappname-yourdomain.rhcloud.com
    [snip]

    $ git remote add oo_yourappname ssh://569f5cf500045f6a1839a0a4@yourappname-yourdomain.rhcloud.com/~/git/yourappname.git/

If you want, set up a branch it should auto-deploy when pushed::

    $ rhc app-configure -a yourappname --deployment-branch openshift

Then, it'll auto-deploy on a receive hook when you push that branch, ie. with
``git push oo_yourappname openshift``. Else, you can always deploy a given git
ref as such::

    $ rhc app-deploy some_git_ref -a yourappname

To fill up the representatives database table, either wait for the cron script
to be executed, either do it manually::

    $ rhc ssh app-root/runtime/repo/.openshift/cron/daily/update_database -a yourappname

OpenShift is fun, login with ssh and look around if you're curious, you'll be
able to recreate your app without much effort if you break it anyway.
