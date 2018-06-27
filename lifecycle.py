def generate_lifecycle():
    """Generate an opinionated S3 lifecycle policy"""
    template = """
    <LifecycleConfiguration>
       <Rule>
          <ID>%(id)s</ID>
          <Status>%(status)s</Status>
          <Filter/>
          <NoncurrentVersionExpiration>
             <NoncurrentDays>%(noncurrentdays)s</NoncurrentDays>
          </NoncurrentVersionExpiration>
       </Rule>
    </LifecycleConfiguration>
    """
    # print("template\n" + template)

    # Squash template so we have a clean, single line xml for encoding
    template = template.replace('\n', '')
    template = template.replace(' ', '')
    data = {'id':'DeleteNonCurrentVersionsAfter60Days', 'status':'Enabled', 'noncurrentdays':'60'}
    payload = template%data
    # print("payload\n" + payload)
    return payload
