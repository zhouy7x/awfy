if __name__ == "__main__":
    env = os.environ.copy()
    req_cset = sys.argv[2]
    with utils.FolderChanger(sys.argv[1]):
        Run('git', 'fetch')
        Run('git', 'reset', '--hard', req_cset)
        Run(['tools/build.py', '--target-arch=x86_64', '--buildtype=release'], env)

        
