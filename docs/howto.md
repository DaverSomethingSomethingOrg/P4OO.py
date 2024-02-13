# P4OO.py - HOWTO

## Initializing a connection

### Using dependency injection

Dependency injection is the most straightforward way to initialize
P4OO, giving clear and direct control to the caller.

#### Establish a connection using P4Python

```python
p4Handle = P4.P4(port="p4-server:1666", user="perforce_user").connect()
```

#### Create P4OO.py objects using that connection

When constructing any P4OO.py object, simply pass in your p4Handle
object as p4PythonObj

```python
changeCounter = P4OOCounter(id="change", p4PythonObj=p4Handle)
```

  OR

```python
lastSubmittedChange = P4OOChangeSet(p4PythonObj=p4Handle).query(status="submitted", max=1)[0]
```

### Using the environment or p4 defaults

Just like `p4` and P4Python, P4OO.py can be used without any special
initialization.  P4OO.py will provide its own P4Python connection and
work with P4Python's defaults or environment.

No special syntax, just construct P4OO.py objects without passing in
the `p4PythonObj` argument.

```python
changeCounter = P4OOCounter(id="change")
```

WARNING: When using defaults, watch out for P4 environment changes
between calls.  You may get inconsistent results across different
P4OO.py objects as they get initialized with different connections.

### Connection persistence

As new P4OO.py objects are returned from P4OO.py operations, they are
seeded with the connection attributes of the object creating them.
Objects created from different connections can be used simultaneously
without conflict.

### Working with multiple connections simultaneously

In an offline backup situation, we might want to examine our offline
replica and compare its content to our production server.  With P4OO.py
it is very easy to accomplish this.

```python
offlineP4Port = "rsh:%s -r %s -J off -i" % (p4d_bin, p4Root,)

offlineP4Handle = P4.P4(port=offlineP4Port, user=p4SysUser).connect()
masterP4Handle = P4.P4(port=masterP4Port, user=p4SysUser).connect()

offlineJournalCounter = P4OOCounter(id="journal", p4PythonObj=offlineP4Handle)
masterJournalCounter = P4OOCounter(id="journal", p4PythonObj=masterP4Handle)
```

## Working with P4OO.py Objects

### Objects as arguments

In P4OO.py, P4OO.py objects can be passed around as arguments to operations
on other objects.  Where a client name or user name is required, the string
name can be provided.  A P4OO.py object identified by that id may also
be provided, it is not necessary to serialize objects within P4OO.py.

#### Example

Given these variables:

```python
userName = "dave"
p4UserObj = P4OOCounter(id=userName, p4PythonObj=p4Handle)
```

The following will produce the same results:

```python
userClients = P4OOClientSet(p4PythonObj=p4Handle).query(user=userName)
userClients = P4OOClientSet(p4PythonObj=p4Handle).query(user=p4UserObj)
```

### Lazy Initialization and Caching for Performance

Wherever possible, P4OO.py uses lazy initialization.  Specs are not
read until attributes are requested from the spec.  Additionally, spec
attributes are cached once read.  Changes to specs made within P4OO.py
will clear the cache as appropriate, but changes outside of P4OO.py may
cause inconsistency.  No accommodation is made for thread safety, it's
fair to assume P4OO.py is not at all thread safe.

### Parsing, parsing, parsing

P4OO.py avoids parsing as much as possible, but in some cases it simply
cannot be avoided.  P4Python is a handy interface into Perforce, but it
sometimes resembles commandline output a little bit too much.  When
creating or deleting a spec it will return a string describing what it
did or did not accomplish for instance, and P4OO.py has to parse that
output.  P4OO.py does leverage P4Python's ability to accept list
parameters in command execution, and so it does not need nor attempt
to construct properly escaped commandlines.  P4OO.py parses so you don't
have to.

### Querying Perforce

#### Querying all objects for specific attributes

Perforce querying is provided by the `_P4OOSet.query()` method.  It is
inherited by all `_P4OOSet` subclasses directly, and `_P4OOSpec`
subclasses can access it through a helper method in `_P4OOBase`.
The easiest way to use it is to create an empty set object to call query
against.

For instance, to find the last submitted change, the query would look like this:

```python
emptySet = P4OOChangeSet(p4PythonObj=p4Handle)
submittedChangeSet = emptySet.query(status="submitted", max=1)
lastSubmittedChangeObj = submittedChangeSet[0]
```

or more directly:

```python
lastSubmittedChangeObj = P4OOChangeSet(p4PythonObj=p4Handle).query(status="submitted", max=1)[0]
```

The supported attributes for query are the same that the 'p4 changes'
command supports, and are documented in each module as well as a
comprehensive table below.

#### Notes on Querying

##### Owner and User attributes

`Owner` and `User` attributes are not used entirely consistently within
Perforce.  For instance, `p4 branch -o <branch_name>` will return a
`Owner` attribute, but `p4 branches` takes a `-u <user>` argument.
With `p4 change`, the attribute is named `User` instead of `Owner`.

P4OO.py attempts to mitigate this partially by allowing `user` to be
queried as `owner` for `P4OOBranchSet`, `P4OOChangeSet`, `P4OOClientSet`,
and `P4OOLabelSet`.  P4OO.py does NOT allow the returned object's
attribute to be fetched by anything other than its native name however.

## Custom Extensions for common Perforce functions

P4OO.py is not merely a replacement for executing `p4` or P4Python calls
and parsing output.  Since first class objects are provided for each
modeled table, each object can be extended to provide new methods,
generalizing common behaviors.

For example, deleting a user completely from Perforce can be a long
series of commands for an admin.  Pending changes and shelved files have
to be cleaned up, clients need to be removed, and so on.  The procedure
is also easily automated since there is a standard algorithm.  With
P4OO.py, it's simply a method call on a `P4OOUser` object that
implements the algorithm, leveraging similar cleanup methods on
`P4OOChange` and `P4OOClient` objects as necessary.

By providing these method extensions, P4OO.py offers far richer API
potential for working with Perforce.

### Labels

#### Find the latest change\# on a given label

```bash
p4 changes -m 1 @<label>
```

 OR

```python
p4LabelObj.getLastChange()
```

### Users

#### Find opened files for a user

##### Across all client workspaces

```python
p4UserObj.listOpenedFiles()
```

##### In a specific client workspace

```python
p4UserObj.listOpenedFiles(client=p4ClientObj)
```

 OR

```python
p4ClientObj.getOpenedFiles(user=p4UserObj)
```

#### Find all clients belonging to a user

```python
p4UserObj.listClients()
```

  OR

```python
P4OOClientSet().query(user=p4UserObj)
```

#### Find all changes owned by a user

```python
p4UserObj.listChanges()
```

  OR

```python
P4OOChangeSet().query(user=p4UserObj)
```

#### Delete user, doing all necessary steps in the process

Deleting a Perforce user is rarely as simple as removing the user spec.
If the user has opened files, shelved files, existing client workspaces,
or pending changes, those need to be addressed before the user can be
removed.

The algorithm works as follows (simplified for illustration):

```bash
for client in `p4 clients -u $user`
    p4 -c $client revert -k //$client/...

for change in `p4 changes -u $user -s pending`
    client = `p4 -ztag change -o 131 |grep -i client`
    p4 -c $client shelve -d -f -c $change
    p4 change -d -f $change

for client in `p4 clients -u $user`
    p4 client -d -f $client

p4 user -d -f $user
```

The equivalent as implemented in P4OO.py:

```python
p4UserObj.deleteWithVengeance()
```
