# Name: Jacob Stewart
# OSU Email: Stewarj8@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/13/2025
# Description: to implement an optimized HashMap using a dynamic array and a
# chaining mechanism for collision resolution. the Chains of key/Value pairs
# will be stored in linked list nodes.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """Updates the key/value pair in the hash map, if the key exists the
        value is updated.
        """
        if self.table_load() > 0.5:
            new_capacity = self._capacity*2
            self.resize_table(new_capacity)

        index = self._hash_function(key) % self._capacity
        hash_kv = HashEntry(key, value)

        if self._buckets[index] is None:
            self._buckets.set_at_index(index, hash_kv)
            self._size += 1
        else:
            j = 1
            quad_index = index
            while self._buckets[quad_index] is not None:
                if self._buckets[quad_index].key == key:
                    if self._buckets[quad_index].is_tombstone:
                        self._buckets.set_at_index(quad_index, hash_kv)
                        self._size += 1
                        self._buckets.get_at_index(quad_index).is_tombstone = False
                    else:
                        self._buckets.set_at_index(quad_index, hash_kv)
                    return

                quad_index = (index + j **2) % self._capacity
                j += 1

            self._buckets.set_at_index(quad_index, hash_kv)
            self._size += 1


    def resize_table(self, new_capacity: int) -> None:
        """Changes the capacity of the original HashMap and all the new
        key/value pairs will be rehashed into the new capacity sized table
        """
        if new_capacity <= self._size:
            return

        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        new_hash = HashMap(new_capacity, self._hash_function)
        if new_capacity == 2:
            new_hash._capacity = 2
        for buckets in self:
            new_hash.put(buckets.key, buckets.value)

        self._buckets = new_hash._buckets
        self._capacity = new_hash._capacity
        self._size = new_hash._size


    def table_load(self) -> float:
        """Returns the current HashMap load factor lamda = n/m
        lamda is load factor, n is total elements in table and
        m is # of buckets
        """
        return self._size/self._capacity


    def empty_buckets(self) -> int:
        """Counts the number of empty buckets
        """
        number_buckets = 0
        for i in range(self._capacity):
            if self._buckets[i] is None or self._buckets[i].is_tombstone:
                number_buckets += 1
        return number_buckets


    def get(self, key: str) -> object:
        """returns the value of a given key
        """
        for i in range(self.get_capacity()):
            if self._buckets[i] is not None:
                if self._buckets[i].key == key and not self._buckets[i].is_tombstone:
                    return self._buckets[i].value
        return None


    def contains_key(self, key: str) -> bool:
        """Checks the Buckets for the given key then returns true if found
        """
        for i in range(self.get_capacity()):
            if self._buckets[i] is not None:
                if self._buckets[i].key == key and not self._buckets[i].is_tombstone:
                    return True
        return False


    def remove(self, key: str) -> None:
        """takes the key passed in and searches through the buckets and
        removes said key/value pair.
        """
        for i in range(self.get_capacity()):
            if self._buckets[i] is not None:
                if self._buckets[i].key == key and not self._buckets[i].is_tombstone:
                    self._buckets[i].is_tombstone = True
                    self._size -= 1


    def get_keys_and_values(self) -> DynamicArray:
        """Returns all the key/value pairs in the Hashmap as a tuple in a
        dynamic array.
        """
        new_da = DynamicArray()

        for i in range(self.get_capacity()):
            if self._buckets[i] is not None:
                if self._buckets[i].is_tombstone is False:
                    new_da.append((self._buckets[i].key, self._buckets[i].value))
        return new_da


    def clear(self) -> None:
        """gets rid of all the Key/Value pairs in the hashmap but doesn't
        change the capacity.
        """
        self._buckets = DynamicArray()
        for i in range(self.get_capacity()):
            self._buckets.append(None)
        self._size = 0


    def __iter__(self):
        """This method is able to iterate across the HashMap by return the
        index value
        """
        self.index = 0
        return self


    def __next__(self):
        """This method updates the index value from the __iter__ method,
        and returns the value.
        """
        try:
            value = None
            while value is None or value.is_tombstone is True:
                value = self._buckets[self.index]
                self.index += 1
        except DynamicArrayException:
            raise StopIteration
        return value


# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
