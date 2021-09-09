def func(backend_kwargs=None, **kwargs):
    if backend_kwargs is not None:
        kwargs.update(backend_kwargs)
    print(kwargs)
    return None


if __name__ == "__main__":
    func()
